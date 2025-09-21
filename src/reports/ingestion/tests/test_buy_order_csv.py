from decimal import Decimal

import pytest
from django.db.models import Sum
from pandas.api.types import is_datetime64_any_dtype

from buy_order.models import BuyOrder
from customer.models import Customer
from reports.ingestion.buy_order_csv.schemas import COLUMN_ALIASES


def test_extract(raw_buy_orders_df):
    df = raw_buy_orders_df

    rows_len = 11

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


@pytest.mark.django_db
def test_customer_cpf_update(loaded_buy_orders):
    cpf = '82312314727'
    customer = Customer.objects.get(cpf=cpf)

    assert customer.first_name == 'bruna'


@pytest.mark.django_db
def test_customer_name_update(loaded_buy_orders):
    email = 'letsilvasantos25@gmail.com'
    customer = Customer.objects.get(email=email)

    assert customer.first_name == 'ana'
    assert customer.last_name == 'santos silva'


@pytest.mark.django_db
def test_customer_group_update(loaded_buy_orders):
    email = 'vivi87.monteiro@gmail.com'
    customer = Customer.objects.get(email=email)

    assert customer.customer_group.name == 'influencer'


@pytest.mark.django_db
def test_customer_amounts(loaded_buy_orders):
    email = 'vivi87.monteiro@gmail.com'
    customer = Customer.objects.get(email=email)

    totals = customer.buy_orders.aggregate(
        total_amount=Sum('total_amount'),
        shipping_amount=Sum('shipping_amount'),
        discount_amount=Sum('discount_amount'),
    )

    assert totals['shipping_amount'] == Decimal('62.87')
    assert totals['discount_amount'] == Decimal('10.00')
    assert totals['total_amount'] == Decimal('760.78')


@pytest.mark.django_db
def test_buy_order_status_update(loaded_buy_orders):
    order_number = '100000010'
    buy_order = BuyOrder.objects.get(order_number=order_number)

    assert buy_order.status.name == 'enviado'
