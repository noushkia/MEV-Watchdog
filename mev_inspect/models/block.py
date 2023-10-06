from sqlalchemy import Column, Integer, Float

from mev_inspect.models.base import Base


class BlockModel(Base):
    __tablename__ = 'blocks'

    block_number = Column(Integer, primary_key=True)
    avg_gas_price = Column(Float)
    avg_gas_usage = Column(Float)
