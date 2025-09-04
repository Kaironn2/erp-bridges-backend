from decimal import Decimal

import pandas as pd
import pytest
from pandas.api.types import is_datetime64_any_dtype

from mgt.ingestion.buy_order_csv.extractor import BuyOrderCsvExtractor
from mgt.ingestion.buy_order_csv.schemas import COLUMN_ALIASES
from mgt.ingestion.buy_order_csv.transformer import BuyOrderCsvTransformer


@pytest.fixture
def buy_orders_dataframe(mgt_fixtures_path) -> pd.DataFrame:
    csv_path = mgt_fixtures_path / 'buy_orders.csv'
    extractor = BuyOrderCsvExtractor(csv_file=csv_path)
    return extractor.extract()


def test_extract(mgt_fixtures_path):
    csv_path = mgt_fixtures_path / 'buy_orders.csv'
    extractor = BuyOrderCsvExtractor(csv_file=csv_path)
    df = extractor.extract()

    rows_len = 1000

    assert len(df) == rows_len
    assert set(df.columns) == set(COLUMN_ALIASES.values())
    assert df.iloc[0]['first_name'] == 'Giovanna'
    assert 'totais' not in df['order_number'].str.lower().unique()


def test_transform(buy_orders_dataframe):
    transformer = BuyOrderCsvTransformer(buy_orders_dataframe)
    df = transformer.transform()

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
