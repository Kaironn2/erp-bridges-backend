import io
from datetime import datetime
from decimal import Decimal

import pytest

from mgt.schemas.buy_orders_report_schema import BuyOrderReportData
from reports.adapters.mgt.buy_orders_csv_adapter import MgtBuyOrdersCsvAdapter


def test_successful_processing(buy_orders_valid_csv_data):
    """Tests that a valid CSV is processed correctly, yielding the expected number of objects."""
    csv_buffer = io.StringIO(buy_orders_valid_csv_data)
    adapter = MgtBuyOrdersCsvAdapter(csv_buffer)

    validated_data = adapter.process()

    buy_orders_len = 2
    assert len(validated_data) == buy_orders_len
    assert isinstance(validated_data[0], BuyOrderReportData)


def test_buy_order_data(validated_buy_orders):
    """Verifies that the report data has been processed correctly"""
    order = validated_buy_orders[0]

    assert order.order_number == '507943839'
    assert order.status == 'cancelado'
    assert order.tracking_code == 'TRACK123'


def test_currency_columns_conversion(validated_buy_orders):
    """Ensures date strings are correctly converted to Decimal objects."""
    order = validated_buy_orders[0]

    assert order.shipping_amount == Decimal('23.24')
    assert order.discount == Decimal('0.00')
    assert order.total_amount == Decimal('85.46')


def test_datetime_columns_conversion(validated_buy_orders):
    """Ensures date strings are correctly converted to datetime objects."""
    order = validated_buy_orders[0]

    assert order.order_date == datetime(2025, 4, 10, 22, 1, 33)


def test_customer_data(validated_buy_orders):
    """Verifies that the report customer data has been processed correctly"""
    order = validated_buy_orders[0]

    assert order.first_name == 'luiza'
    assert order.last_name == 'correia'
    assert order.email == 'luigi32@viana.br'
    assert order.cpf == '09176482340'
    assert order.phone == '7163794026'


def test_columns_remapping(validated_buy_orders):
    """Verifies if column data has been correcly remapped"""
    order = validated_buy_orders[0]

    assert order.payment_type == 'boleto bancário'


def test_empty_strings_converted_to_none(buy_orders_valid_csv_data):
    """Checks if empty strings are converted to None after cleaning process

    Args:
        buy_orders_valid_csv_data (_type_): fixture with valid csv data
    """
    csv_buffer = io.StringIO(buy_orders_valid_csv_data)
    adapter = MgtBuyOrdersCsvAdapter(csv_buffer)

    validated_data = adapter.process()

    order3 = validated_data[1]
    assert order3.phone is None


def test_file_not_found_raises_error():
    """
    Tests that instantiating the adapter with a non-existent file path
    correctly raises a ValueError.
    """
    with pytest.raises(ValueError, match='File not found in the path'):
        MgtBuyOrdersCsvAdapter('inexistent/csv_path.csv')


def test_invalid_data_raises_validation_error(buy_orders_data_with_missing_required_field):
    """
    Checks whether a ValueError from Pydantic ValidatioError when a field is missing

    Args:
        buy_orders_data_with_missing_required_field (str): fixture with data missing one field
    """
    csv_buffer = io.StringIO(buy_orders_data_with_missing_required_field)
    adapter = MgtBuyOrdersCsvAdapter(csv_buffer)

    with pytest.raises(ValueError, match='Pydantic validation error'):
        adapter.process()


def test_empty_or_header_only_file_returns_empty_list(buy_orders_header_only_csv_data):
    """
    tests whether an empty list is returned when csv has no data
    other than the headers

    Args:
        buy_orders_header_only_csv_data (_type_): empty data csv fixture, only headers
    """
    csv_buffer = io.StringIO(buy_orders_header_only_csv_data)
    adapter = MgtBuyOrdersCsvAdapter(csv_buffer)

    validated_data = adapter.process()

    assert validated_data == []
