import json
import logging
from typing import List

from sqlalchemy import orm

from mev_inspect.models.liquidations import LiquidationModel
from mev_inspect.schemas.liquidations import Liquidation


def write_liquidations(
        liquidations: List[Liquidation],
        db_session: orm.Session
) -> None:
    liquidation_instances = [
        LiquidationModel(**json.loads(liquidation.json()))
        for liquidation in liquidations
    ]

    try:
        db_session.bulk_save_objects(liquidation_instances)
        db_session.commit()
    except Exception as e:
        db_session.rollback()
        print(f"Liquidations: An error occurred while saving liquidations: {e}")
