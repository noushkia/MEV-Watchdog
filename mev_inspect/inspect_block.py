import configparser
import logging
from pathlib import Path
from typing import List

from sqlalchemy import orm
from web3 import Web3

from mev_inspect.arbitrages import get_arbitrages
from mev_inspect.block import create_from_block_number
from mev_inspect.classifiers.trace import TraceClassifier
from mev_inspect.crud.arbitrages import write_arbitrages
from mev_inspect.crud.liquidations import write_liquidations
from mev_inspect.crud.blocks import write_blocks_features
from mev_inspect.liquidations import get_liquidations
from mev_inspect.schemas.arbitrages import Arbitrage
from mev_inspect.schemas.blocks import Block
from mev_inspect.schemas.liquidations import Liquidation
from mev_inspect.schemas.swaps import Swap
from mev_inspect.swaps import get_swaps
from mev_inspect.utils import get_handler

config = configparser.ConfigParser()
config.read('config.ini')

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s %(levelname)s:%(message)s')

console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)
console_handler.setFormatter(formatter)

logger.addHandler(console_handler)


async def inspect_many_blocks(
        w3: Web3,
        trace_classifier: TraceClassifier,
        after_block_number: int,
        before_block_number: int,
        host: str,
        inspect_db_session: orm.Session,
) -> None:
    logs_path = Path(config['logs']['logs_path']) / config['logs']['inspectors_log_path'] / f"inspector_{host}.log"
    logger.addHandler(get_handler(logs_path, formatter, rotate=True))

    all_blocks: List[Block] = []
    all_swaps: List[Swap] = []
    all_arbitrages: List[Arbitrage] = []
    all_liquidations: List[Liquidation] = []
    all_address_activity = {}

    logger.info(f"Inspecting blocks {after_block_number} to {before_block_number}")
    for block_number in range(after_block_number, before_block_number):
        logger.debug(f"Block: {block_number} -- Getting block data")

        block, address_activity = await create_from_block_number(w3, block_number)

        classified_traces = trace_classifier.classify(block.traces)

        swaps = get_swaps(classified_traces)
        logger.debug(f"Block: {block_number} -- Found {len(swaps)} swaps")

        arbitrages = get_arbitrages(swaps)
        logger.debug(f"Block: {block_number} -- Found {len(arbitrages)} arbitrages")

        liquidations = get_liquidations(classified_traces)
        logger.debug(f"Block: {block_number} -- Found {len(liquidations)} liquidations")

        all_blocks.append(block)
        all_address_activity.update(address_activity)
        all_swaps.extend(swaps)
        all_arbitrages.extend(arbitrages)
        all_liquidations.extend(liquidations)

    logger.debug("Writing to DB")

    write_blocks_features(all_blocks, inspect_db_session)
    write_arbitrages(all_arbitrages, inspect_db_session)
    write_liquidations(all_liquidations, inspect_db_session)

    logger.debug("Writing done")
