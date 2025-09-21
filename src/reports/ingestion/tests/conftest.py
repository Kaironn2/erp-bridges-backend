from pathlib import Path

import pandas as pd
import pytest
from django.conf import settings

from reports.ingestion.buy_order_csv.extractor import BuyOrderCsvExtractor
from reports.ingestion.buy_order_csv.loader import BuyOrderCsvLoader
from reports.ingestion.buy_order_csv.transformer import BuyOrderCsvTransformer
from reports.ingestion.customer_csv.extractor import CustomerCsvExtractor
from reports.ingestion.customer_csv.loader import CustomerCsvLoader
from reports.ingestion.customer_csv.transformer import CustomerCsvTransformer
from reports.ingestion.ecs_buy_order_csv.extractor import EcsBuyOrderCsvExtractor
from reports.ingestion.ecs_buy_order_csv.transformer import EcsBuyOrderCsvTransformer
from reports.ingestion.ecs_buy_order_csv.loader import EcsBuyOrderCsvLoader


@pytest.fixture
def data_tests_folder() -> Path:
    """Returns data tests folder path"""
    return Path(settings.BASE_DIR) / 'reports' / 'ingestion' / 'tests' / 'fixtures'


@pytest.fixture
def raw_buy_orders_df(data_tests_folder: Path) -> pd.DataFrame:
    """Extracts and returns the raw DataFrame from the CSV file."""
    csv_path = data_tests_folder / 'buy_orders.csv'
    extractor = BuyOrderCsvExtractor(csv_file=csv_path)
    return extractor.extract()


@pytest.fixture
def transformed_buy_orders_df(raw_buy_orders_df: pd.DataFrame) -> pd.DataFrame:
    """Transforms the raw DataFrame into a clean, ready-to-load format."""
    transformer = BuyOrderCsvTransformer(raw_buy_orders_df)
    return transformer.transform()


@pytest.fixture
@pytest.mark.django_db
def loaded_buy_orders(transformed_buy_orders_df: pd.DataFrame) -> None:
    """Loads the transformed DataFrame into the database."""
    loader = BuyOrderCsvLoader(transformed_buy_orders_df)
    loader.load()


@pytest.fixture
def raw_customers_df(data_tests_folder: Path) -> pd.DataFrame:
    """Extracts and returns the raw DataFrame from the CSV file."""
    csv_path = data_tests_folder / 'customers.csv'
    extractor = CustomerCsvExtractor(csv_file=csv_path)
    return extractor.extract()


@pytest.fixture
def transformed_customers_df(raw_customers_df: pd.DataFrame) -> pd.DataFrame:
    """Transforms the raw DataFrame into a clean, ready-to-load format."""
    transformer = CustomerCsvTransformer(raw_customers_df)
    return transformer.transform()


@pytest.fixture
@pytest.mark.django_db
def loaded_customers(transformed_customers_df: pd.DataFrame) -> None:
    """Loads the transformed DataFrame into the database."""
    loader = CustomerCsvLoader(transformed_customers_df)
    loader.load()


@pytest.fixture
def raw_ecs_buy_orders_df(data_tests_folder: Path) -> pd.DataFrame:
    """Extracts and returns the raw DataFrame from the CSV file."""
    csv_path = data_tests_folder / 'ecs_buy_orders.csv'
    extractor = EcsBuyOrderCsvExtractor(csv_file=csv_path)
    return extractor.extract()


@pytest.fixture
def transformed_ecs_buy_orders_df(raw_ecs_buy_orders_df: pd.DataFrame) -> pd.DataFrame:
    """Transforms the raw DataFrame into a clean, ready-to-load format."""
    transformer = EcsBuyOrderCsvTransformer(raw_ecs_buy_orders_df)
    return transformer.transform()


@pytest.fixture
@pytest.mark.django_db
def loaded_ecs_buy_orders(transformed_ecs_buy_orders_df: pd.DataFrame) -> None:
    """Loads the transformed DataFrame into the database."""
    loader = EcsBuyOrderCsvLoader(transformed_ecs_buy_orders_df)
    loader.load()
