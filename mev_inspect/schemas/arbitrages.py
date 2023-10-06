from typing import List

from pydantic import BaseModel

from .swaps import Swap


class Arbitrage(BaseModel):
    swaps: List[Swap]
    block_number: int
    timestamp: str
    transaction_hash: str
    account_address: str
    status: bool
    contracts_address: List[str]
    input_tokens_address: List[str]
    input_tokens_amount: List[float]
    output_tokens_address: List[str]
    output_tokens_amount: List[float]
    gas_price: int
    gas_usage: int
    block_position: int

    def profit_amount(self) -> float:
        # todo
        #  gather every token transferred into the account_address during the swaps
        #  calculate the tokens transferred out of the account_address (beware of different tokens values!)
        #  provide either a list of all tokens transferred as pure revenue or total profit using exchange rates
        return self.output_tokens_amount[-1] - self.input_tokens_amount[0]
