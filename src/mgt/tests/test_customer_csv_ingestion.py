from datetime import datetime

from django.utils import timezone
import pandas as pd
from pandas.api.types import is_datetime64_any_dtype
import pytest

from mgt.ingestion.customer_csv.extractor import CustomerCsvExtractor
from mgt.ingestion.customer_csv.loader import CustomerCsvLoader
from mgt.ingestion.customer_csv.transformer import CustomerCsvTransformer
from mgt.ingestion.customer_csv.schemas import COLUMN_ALIASES
from mgt.models import Customer


@pytest.fixture
def customers_dataframe(mgt_fixtures_path) -> pd.DataFrame:
    csv_path = mgt_fixtures_path / 'customers.csv'
    extractor = CustomerCsvExtractor(csv_file=csv_path)
    return extractor.extract()


def test_extract(mgt_fixtures_path):
    csv_path = mgt_fixtures_path / 'customers.csv'
    extractor = CustomerCsvExtractor(csv_file=csv_path)
    df = extractor.extract()

    rows_len = 10000

    assert len(df) == rows_len
    assert set(df.columns) == set(COLUMN_ALIASES.values())
    assert df.iloc[0]['name'] == 'Maria Clara Rios'


def test_transform(customers_dataframe):
    transformer = CustomerCsvTransformer(customers_dataframe)
    df = transformer.transform()

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

    columns_to_check_digits = ['phone']
    for column in columns_to_check_digits:
        series = df[column].dropna()
        assert series.str.isdigit().all(), f"Column '{column}' contains non-digit characters."


@pytest.mark.django_db
def test_load(customers_dataframe):
    transformer = CustomerCsvTransformer(customers_dataframe)
    df = transformer.transform()
    loader = CustomerCsvLoader(df)
    loader.load()

    total_customers = 9512
    assert Customer.objects.count() == total_customers

    first_customer = Customer.objects.order_by('external_id').first()
    assert first_customer is not None

    expected_customer_since = timezone.make_aware(datetime(2023, 11, 4, 9, 8, 44))
    assert first_customer.first_name == 'maria'
    assert first_customer.external_id == '191511'
    assert first_customer.customer_since == expected_customer_since
