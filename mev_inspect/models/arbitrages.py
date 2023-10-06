from sqlalchemy import Column, Integer, String, Boolean, Float, BigInteger

from mev_inspect.models.base import Base


class ArbitrageModel(Base):
    __tablename__ = 'arbitrages'

    id = Column(Integer, primary_key=True, index=True)
    transaction_hash = Column(String(100))
    block_number = Column(Integer)
    timestamp = Column(String(50))
    account_address = Column(String(100))
    status = Column(Boolean)
    contracts_address = Column(String(500))
    input_tokens_address = Column(String(500))
    input_tokens_amount = Column(String(500))
    output_tokens_address = Column(String(500))
    output_tokens_amount = Column(String(500))
    protocols = Column(String(500))
    gas_price = Column(BigInteger)
    gas_usage = Column(Integer)
    block_position = Column(Integer)
    profit_amount = Column(Float)

    def __str__(self) -> str:
        return f"{self.block_number},{self.timestamp},{self.transaction_hash},{self.account_address},{self.status}," \
               f"{self.contracts_address},{self.input_tokens_address},{self.input_tokens_amount}," \
               f"{self.output_tokens_address},{self.output_tokens_amount},{self.protocols}," \
               f"{self.gas_price},{self.gas_usage},{self.block_position}"

