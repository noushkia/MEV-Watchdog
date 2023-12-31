import asyncio
import configparser
import logging
import traceback
from asyncio import CancelledError, Queue
from pathlib import Path

from sqlalchemy import orm, desc
from sqlalchemy.orm import Session

from web3 import Web3
from web3.eth import AsyncEth

from mev_inspect.classifiers.trace import TraceClassifier
from mev_inspect.inspect_block import inspect_many_blocks
from mev_inspect.methods import get_block_receipts, trace_block
from mev_inspect.models.block import BlockModel
from mev_inspect.provider import get_base_provider

config = configparser.ConfigParser()
config.read('config.ini')

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s %(levelname)s:%(message)s')

# add missing parity methods
AsyncEth.trace_block = trace_block
AsyncEth.get_block_receipts = get_block_receipts


def _get_last_inspected_block(session: Session, after_block: int, before_block: int) -> int:
    """
    Gets the last block that was inspected and stored on DB.
    Might be better to modify it and move it to pre-exec stages.
    """
    latest_block = session.query(BlockModel.block_number) \
        .filter(BlockModel.block_number < before_block) \
        .order_by(desc(BlockModel.block_number)) \
        .first()
    if latest_block is not None and latest_block[0] > after_block:
        after_block = latest_block[0] + 1

    return after_block


class MEVInspector:
    def __init__(
            self,
            rpc: str,
            max_concurrency: int = 1,
            request_timeout: int = 300,
    ):
        base_provider = get_base_provider(rpc, request_timeout=request_timeout)
        self.w3 = Web3(base_provider, modules={"eth": (AsyncEth,)}, middlewares=[])
        self.host = rpc.split(":")[1].strip("/")
        self.trace_classifier = TraceClassifier()
        self.max_concurrency = max_concurrency
        self.batch_queue = Queue()

    async def inspect_many_blocks(
            self,
            inspect_db_session: orm.Session,
            after_block: int,
            before_block: int,
            block_batch_size: int = 20,
    ):
        after_block = _get_last_inspected_block(inspect_db_session, after_block, before_block)

        tasks = []
        sem = asyncio.Semaphore(self.max_concurrency)
        for block_number in range(after_block, before_block, block_batch_size):
            batch_after_block = block_number
            batch_before_block = min(block_number + block_batch_size, before_block)
            tasks.append(
                asyncio.ensure_future(
                    self.safe_inspect_many_blocks(
                        inspect_db_session=inspect_db_session,
                        after_block_number=batch_after_block,
                        before_block_number=batch_before_block,
                        semaphore=sem
                    )
                )
            )

        logger.info(f"{self.host}: Gathered {before_block - after_block} blocks to inspect")
        try:
            await asyncio.gather(*tasks)
        except CancelledError:
            logger.info(f"{self.host}: Requested to exit, cleaning up...")
        except Exception:
            logger.error(f"{self.host}: Exited due to {traceback.print_exc()}")
            raise

    async def safe_inspect_many_blocks(
            self,
            inspect_db_session: orm.Session,
            after_block_number: int,
            before_block_number: int,
            semaphore: asyncio.Semaphore,
    ):
        async with semaphore:
            await self.batch_queue.put(await inspect_many_blocks(
                self.w3,
                self.trace_classifier,
                after_block_number,
                before_block_number,
                host=self.host,
                inspect_db_session=inspect_db_session,
            ))
