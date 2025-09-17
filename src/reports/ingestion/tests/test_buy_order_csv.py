from decimal import Decimal
from pathlib import Path

import pandas as pd
import pytest
from pandas.api.types import is_datetime64_any_dtype

from buy_order.models import BuyOrder
from customer.models import Customer
from reports.ingestion.buy_order_csv.extractor import BuyOrderCsvExtractor
from reports.ingestion.buy_order_csv.loader import BuyOrderCsvLoader
from reports.ingestion.buy_order_csv.schemas import COLUMN_ALIASES
from reports.ingestion.buy_order_csv.transformer import BuyOrderCsvTransformer


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


def test_extract(raw_buy_orders_df):
    df = raw_buy_orders_df

    rows_len = 10

    assert len(df) == rows_len
    assert set(df.columns) == set(COLUMN_ALIASES.values())
    assert 'totais' not in df['order_number'].str.lower().unique()


def test_transform(transformed_buy_orders_df):
    df = transformed_buy_orders_df

    columns_to_check_case = ['first_name', 'last_name', 'email', 'customer_group', 'status']
    for column in columns_to_check_case:
        series = df[column].dropna()
        assert (series == series.str.lower()).all(), (
            f"Column '{column}' contains non-lowercase values."
        )

    columns_to_check_decimal = ['shipping_amount', 'discount_amount', 'total_amount']
    for column in columns_to_check_decimal:
        assert all(isinstance(x, Decimal) for x in df[column].dropna()), (
            f"Column '{column}' does not contain only Decimal objects."
        )

    columns_to_check_date = ['order_date']
    for column in columns_to_check_date:
        assert is_datetime64_any_dtype(df[column]), f"Column '{column}' is not a datetime type."
        assert df[column].dt.tz is not None, f"Column '{column}' is not timezone-aware."

    columns_to_check_digits = ['cpf', 'phone']
    for column in columns_to_check_digits:
        series = df[column].dropna()
        assert series.str.isdigit().all(), f"Column '{column}' contains non-digit characters."

    expected_payment_types = {'pix', 'cartão de crédito', 'boleto bancário', 'saldo', None}
    actual_payment_types = set(df['payment_type'].unique())
    assert actual_payment_types.issubset(expected_payment_types)


@pytest.mark.django_db
def test_load_data(loaded_buy_orders):
    total_buy_orders = 10
    total_customers = 4
    assert Customer.objects.count() == total_customers
    assert BuyOrder.objects.count() == total_buy_orders


@pytest.mark.django_db
def test_customer_email_update(loaded_buy_orders):
    email = 'alan_oliveira798@gmail.com'
    customer = Customer.objects.get(email=email)

    assert customer.first_name == 'alan'


# @pytest.mark.django_db
# def test_customer_cpf_update(loaded_buy_orders):
#     cpf = '82312314727'
#     customer = Customer.objects.get(cpf=cpf)

#     assert customer is not None
#     assert customer.first_name == 'bruna'
