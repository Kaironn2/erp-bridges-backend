import pytest
from pandas.api.types import is_datetime64_any_dtype, is_integer_dtype

from buy_order.models import EcsBuyOrder
from reports.ingestion.ecs_buy_order_csv.schemas import COLUMN_ALIASES


def test_extract(raw_ecs_buy_orders_df):
    df = raw_ecs_buy_orders_df

    rows_len = 4

    assert len(df) == rows_len
    assert set(df.columns) == set(COLUMN_ALIASES.values())


def test_transform(transformed_ecs_buy_orders_df):
    df = transformed_ecs_buy_orders_df

    columns_to_check_case = [
        'recipient_name',
        'recipient_city',
        'recipient_state',
        'carrier',
        'coupon',
        'payment_type',
    ]
    for column in columns_to_check_case:
        series = df[column].dropna()
        assert (series == series.str.lower()).all(), (
            f"Column '{column}' contains non-lowercase values."
        )

    columns_to_check_date = ['ecs_delivery_date', 'payment_date']
    for column in columns_to_check_date:
        if df[column].notna().any():
            assert is_datetime64_any_dtype(df[column]), (
                f"Column '{column}' is not a datetime type."
            )
            assert df[column].dtype.tz is not None, f"Column '{column}' is not timezone-aware."

    columns_to_check_digits = ['recipient_zip_code', 'cnpj']
    for column in columns_to_check_digits:
        series = df[column].dropna()
        assert series.str.isdigit().all(), f"Column '{column}' contains non-digit characters."

    columns_to_check_int = ['deadline_days']
    for column in columns_to_check_int:
        assert is_integer_dtype(df[column]), f"Column '{column}' is not integer."

    expected_payment_types = {'pix', 'cartão de crédito', 'boleto bancário', 'saldo', None}
    actual_payment_types = set(df['payment_type'].unique())
    assert actual_payment_types.issubset(expected_payment_types)


@pytest.mark.django_db
def test_load_data(loaded_buy_orders, loaded_ecs_buy_orders):
    total_ecs_buy_orders = 4
    assert EcsBuyOrder.objects.count() == total_ecs_buy_orders


@pytest.mark.django_db
def test_cnpj(loaded_buy_orders, loaded_ecs_buy_orders):
    cnpj = '16854723000112'
    ecs_bo = EcsBuyOrder.objects.get(company__cnpj=cnpj)

    assert ecs_bo.recipient_name == 'rafael santos'
