from datetime import datetime, timezone
from pathlib import Path

import pandas as pd
import pytest
from pandas.api.types import is_datetime64_any_dtype

from customer.models import Customer
from reports.ingestion.customer_csv.extractor import CustomerCsvExtractor
from reports.ingestion.customer_csv.loader import CustomerCsvLoader
from reports.ingestion.customer_csv.schemas import COLUMN_ALIASES
from reports.ingestion.customer_csv.transformer import CustomerCsvTransformer


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


def test_extract(raw_customers_df):
    df = raw_customers_df

    rows_len = 5

    assert len(df) == rows_len
    assert set(df.columns) == set(COLUMN_ALIASES.values())


def test_transform(transformed_customers_df):
    df = transformed_customers_df

    columns_to_check_case = ['first_name', 'last_name', 'email', 'customer_group']
    for column in columns_to_check_case:
        series = df[column].dropna()
        assert (series == series.str.lower()).all(), (
            f"Column '{column}' contains non-lowercase values."
        )

    columns_to_check_date = ['customer_since']
    for column in columns_to_check_date:
        assert is_datetime64_any_dtype(df[column]), f"Column '{column}' is not a datetime type."
        assert df[column].dt.tz is not None, f"Column '{column}' is not timezone-aware."

    columns_to_check_digits = ['phone', 'postal_code']
    for column in columns_to_check_digits:
        series = df[column].dropna()
        assert series.str.isdigit().all(), f"Column '{column}' contains non-digit characters."


@pytest.mark.django_db
def test_load_data(loaded_customers):
    total_customers = 5
    assert Customer.objects.count() == total_customers


@pytest.mark.django_db
def test_loaded_customer_data(loaded_customers):
    email = 'ricardofilho9741@gmail.com'
    customer = Customer.objects.get(email=email)

    assert customer.first_name == 'ricardo'
    assert customer.last_name == 'filho'
    assert customer.customer_group.name == 'vip'
    assert not customer.phone


@pytest.mark.django_db
def test_only_digit_attributes(loaded_customers):
    email = 'luancarvalho741@bol.com.br'
    customer = Customer.objects.get(email=email)

    assert customer.phone == '81999994444'
    assert customer.postal_code == '41520327'


@pytest.mark.django_db
def test_datetime_attributes(loaded_customers):
    email = 'luancarvalho741@bol.com.br'
    customer = Customer.objects.get(email=email)

    assert customer.customer_since == datetime(2025, 9, 18, 12, 10, 16, tzinfo=timezone.utc)
