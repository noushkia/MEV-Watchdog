import asyncio
import datetime
from typing import List, Optional, Dict

from web3 import Web3
from web3.types import TxData

from mev_inspect.fees import fetch_base_fee_per_gas
from mev_inspect.schemas.blocks import Block
from mev_inspect.schemas.receipts import Receipt
from mev_inspect.schemas.traces import Trace, TraceType


async def create_from_block_number(
        w3: Web3,
        block_number: int,
) -> (Block, Dict):
    block_data, receipts, traces, base_fee_per_gas = await asyncio.gather(
        _fetch_block_data(w3, block_number),
        _fetch_block_receipts(w3, block_number),
        _fetch_block_traces(w3, block_number),
        fetch_base_fee_per_gas(w3, block_number),
    )

    block_timestamp, block_transactions = block_data

    miner_address = _get_miner_address_from_traces(traces)
    avg_gas_price, avg_gas_usage, address_activity = _extract_features(block_transactions)

    return Block(
        block_number=block_number,
        block_timestamp=block_timestamp,
        miner=miner_address,
        base_fee_per_gas=base_fee_per_gas,
        traces=_append_block_timestamp(traces, str(datetime.datetime.fromtimestamp(block_timestamp))),
        receipts=receipts,
        avg_gas_price=avg_gas_price,
        avg_gas_usage=avg_gas_usage,
    ), address_activity


async def _fetch_block_data(w3, block_number: int) -> (int, List):
    block_json = await w3.eth.get_block(block_identifier=block_number, full_transactions=True)
    return block_json["timestamp"], block_json["transactions"]


async def _fetch_block_receipts(w3, block_number: int) -> List[Receipt]:
    receipts_json = await w3.eth.get_block_receipts(block_number)
    return [Receipt(**receipt) for receipt in receipts_json]


async def _fetch_block_traces(w3, block_number: int) -> List[Trace]:
    traces_json = await w3.eth.trace_block(block_number)
    return [Trace(**trace_json) for trace_json in traces_json]


def _get_miner_address_from_traces(traces: List[Trace]) -> Optional[str]:
    for trace in traces:
        if trace.type == TraceType.reward:
            return trace.action["author"]
    return None


def _append_block_timestamp(traces: List[Trace], block_timestamp: str) -> List[Trace]:
    for trace in traces:
        trace.block_timestamp = block_timestamp

    return traces


def _extract_features(block_transactions: List[TxData]) -> (float, float, Dict):
    avg_gas_price = 0
    avg_gas_usage = 0
    address_transaction = {}

    txn_cnt = len(block_transactions)
    for transaction in block_transactions:
        avg_gas_price += transaction["gasPrice"] / txn_cnt
        avg_gas_usage += transaction["gas"] / txn_cnt
        address_transaction[transaction["from"]] = address_transaction.get(transaction["from"], 0) + 1

    return avg_gas_price, avg_gas_usage, address_transaction
