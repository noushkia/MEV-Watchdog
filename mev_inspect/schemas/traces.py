from enum import Enum
from typing import Any, Dict, List, Optional

from .utils import CamelModel


class TraceType(Enum):
    call = "call"
    create = "create"
    delegate_call = "delegateCall"
    reward = "reward"
    suicide = "suicide"


class Trace(CamelModel):
    action: dict
    block_hash: str
    block_number: int
    block_timestamp: Optional[str]
    result: Optional[dict]
    subtraces: int
    trace_address: List[int]
    transaction_hash: Optional[str]
    transaction_position: Optional[int]
    type: TraceType
    error: Optional[str]


class Classification(Enum):
    unknown = "unknown"
    swap = "swap"
    transfer = "transfer"
    liquidate = "liquidate"
    seize = "seize"


class Protocol(Enum):
    uniswap_v2 = "uniswap_v2"
    uniswap_v3 = "uniswap_v3"
    sushiswap = "sushiswap"
    aave = "aave"
    weth = "weth"
    curve = "curve"
    balancer_v1 = "balancer_v1"
    compound_v2 = "compound_v2"
    bancor = "bancor"


class ClassifiedTrace(Trace):
    classification: Classification
    to_address: Optional[str]
    from_address: Optional[str]
    gas: Optional[int]
    value: Optional[int]
    gas_used: Optional[int]
    transaction_hash: str
    transaction_position: int
    protocol: Optional[Protocol]
    function_name: Optional[str]
    function_signature: Optional[str]
    inputs: Optional[Dict[str, Any]]
    abi_name: Optional[str]


class CallTrace(ClassifiedTrace):
    to_address: str
    from_address: str


class DecodedCallTrace(CallTrace):
    inputs: Dict[str, Any]
    abi_name: str
    protocol: Optional[Protocol]
    gas: Optional[int]
    gas_used: Optional[int]
    function_name: str
    function_signature: str
