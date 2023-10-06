from typing import List

from sqlalchemy import orm

from mev_inspect.models.block import BlockModel
from mev_inspect.schemas.blocks import Block


def write_blocks_features(
        blocks: List[Block],
        db_session: orm.Session,
) -> None:
    block_models = [
        BlockModel(
            block_number=block.block_number,
            avg_gas_price=block.avg_gas_price,
            avg_gas_usage=block.avg_gas_usage,
        )
        for block in blocks
    ]
    db_session.bulk_save_objects(block_models)
    db_session.commit()
