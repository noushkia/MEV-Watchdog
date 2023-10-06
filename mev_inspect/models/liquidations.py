from sqlalchemy import Column, Integer, String, Boolean, BigInteger

from mev_inspect.models.base import Base


class LiquidationModel(Base):
    __tablename__ = 'liquidations'

    id = Column(Integer, primary_key=True, index=True)
    transaction_hash = Column(String(100))
    block_number = Column(Integer)
    timestamp = Column(String(50))
    trace_address = Column(String(500))
    status = Column(Boolean)
    liquidated_user = Column(String(100))
    liquidator_user = Column(String(100))
    debt_token_address = Column(String(100))
    debt_purchase_amount = Column(String(500))
    received_amount = Column(String(500))
    received_token_address = Column(String(100))
    protocol = Column(String(50))
    gas_price = Column(BigInteger)
    gas_usage = Column(Integer)
    block_position = Column(Integer)

    def __str__(self) -> str:
        return f"{self.transaction_hash},{self.block_number},{self.timestamp},{self.trace_address}," \
               f"{self.status},{self.liquidated_user},{self.liquidator_user},{self.debt_token_address}," \
               f"{self.debt_purchase_amount},{self.received_amount},{self.received_token_address}," \
               f"{self.protocol},{self.gas_price},{self.gas_usage},{self.block_position}"
