import logging
from typing import List

from sqlalchemy import orm

from mev_inspect.models.arbitrages import ArbitrageModel
from mev_inspect.schemas.arbitrages import Arbitrage


def write_arbitrages(
        arbitrages: List[Arbitrage],
        db_session: orm.Session,
) -> None:
    arbitrage_instances = [
        ArbitrageModel(
            transaction_hash=arbitrage.transaction_hash,
            block_number=arbitrage.block_number,
            timestamp=arbitrage.timestamp,
            account_address=arbitrage.account_address,
            status=arbitrage.status,
            contracts_address=arbitrage.contracts_address,
            input_tokens_address=arbitrage.input_tokens_address,
            input_tokens_amount=arbitrage.input_tokens_amount,
            output_tokens_address=arbitrage.output_tokens_address,
            output_tokens_amount=arbitrage.output_tokens_amount,
            protocols=list(set([swap.protocol.value for swap in arbitrage.swaps])),
            gas_price=arbitrage.gas_price,
            gas_usage=arbitrage.gas_usage,
            block_position=arbitrage.block_position,
            profit_amount=arbitrage.profit_amount(),
        )
        for arbitrage in arbitrages
    ]

    try:
        db_session.bulk_save_objects(arbitrage_instances)
        db_session.commit()
    except Exception as e:
        db_session.rollback()
        print(f"Arbitrages: An error occurred while saving liquidations: {e}")

