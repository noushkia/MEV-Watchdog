from typing import List, Optional

from pydantic import BaseModel

from mev_inspect.schemas.traces import Protocol


class Liquidation(BaseModel):
    transaction_hash: str
    block_number: str
    timestamp: str
    trace_address: List[int]
    status: bool
    liquidated_user: str
    liquidator_user: str
    debt_token_address: str
    debt_purchase_amount: int
    received_amount: int
    received_token_address: Optional[str]
    protocol: Protocol
    gas_price: int
    gas_usage: int
    block_position: int
