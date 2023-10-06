from typing import List


class SwapModel:
    def __init__(
            self,
            abi_name: str,
            transaction_hash: str,
            transaction_position: int,
            block_number: int,
            timestamp: str,
            trace_address: List[int],
            protocol: str,
            contract_address: str,
            from_address: str,
            to_address: str,
            token_in_address: str,
            token_in_amount: float,
            token_out_address: str,
            token_out_amount: float,
            error: str,
            gas_price: int,
            gas_usage: int,
    ):
        self.abi_name = abi_name
        self.transaction_hash = transaction_hash
        self.transaction_position = transaction_position
        self.block_number = block_number
        self.timestamp = timestamp
        self.trace_address = list(map(str, trace_address))
        self.protocol = protocol
        self.contract_address = contract_address
        self.from_address = from_address
        self.to_address = to_address
        self.token_in_address = token_in_address
        self.token_in_amount = token_in_amount
        self.token_out_address = token_out_address
        self.token_out_amount = token_out_amount
        self.error = error
        self.gas_price = gas_price
        self.gas_usage = gas_usage

    def to_dict(self):
        return {
            "abi_name": self.abi_name,
            "transaction_hash": self.transaction_hash,
            "transaction_position": self.transaction_position,
            "block_number": self.block_number,
            "timestamp": self.timestamp,
            "trace_address": self.trace_address,
            "protocol": self.protocol,
            "contract_address": self.contract_address,
            "from_address": self.from_address,
            "to_address": self.to_address,
            "token_in_address": self.token_in_address,
            "token_in_amount": self.token_in_amount,
            "token_out_address": self.token_out_address,
            "token_out_amount": self.token_out_amount,
            "error": self.error,
            "gas_price": self.gas_price,
            "gas_usage": self.gas_usage,
        }
