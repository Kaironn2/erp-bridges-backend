import pandas as pd
import pytest

from ecs.ingestion.ecs_order_csv.extractor import EcsOrderCsvExtractor
from mgt.ingestion.buy_order_csv.schemas import COLUMN_ALIASES


@pytest.fixture
def buy_orders_dataframe(ecs_fixtures_path) -> pd.DataFrame:
    csv_path = ecs_fixtures_path / 'ecs_orders.csv'
    extractor = EcsOrderCsvExtractor(csv_file=csv_path)
    return extractor.extract()


def test_extract(ecs_fixtures_path): ...
