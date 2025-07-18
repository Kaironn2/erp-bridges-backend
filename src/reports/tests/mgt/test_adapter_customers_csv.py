import io
from datetime import datetime

import pytest

from mgt.schemas.customers_report_schema import CustomerReportData
from reports.adapters.mgt.customers_csv_adapter import MgtCustomersCsvAdapter


def test_successful_processing(customers_valid_csv_data):
    """Tests that a valid CSV is processed correctly, yielding the expected number of objects."""
    csv_buffer = io.StringIO(customers_valid_csv_data)
    adapter = MgtCustomersCsvAdapter(csv_buffer)

    validated_data = adapter.process()

    customers_len = 4
    assert len(validated_data) == customers_len
    assert isinstance(validated_data[0], CustomerReportData)


def test_columns_split(validated_customers):
    """Verifies that the full name column is correctly split into first and last names."""
    customer1 = validated_customers[0]

    assert customer1.first_name == 'júlya'
    assert customer1.last_name == 'viana'


def test_datetime_columns_conversion(validated_customers):
    """Ensures date strings are correctly converted to datetime objects."""
    customer = validated_customers[0]

    assert isinstance(customer.customer_since, datetime)
    assert customer.customer_since == datetime(2025, 7, 14, 11, 4, 50)


def test_empty_phone_is_none(validated_customers):
    """Tests that a phone field containing only a dash ('-') is processed as None."""
    customer = validated_customers[2]

    assert customer.phone is None


def test_phone_keep_only_digits(validated_customers):
    """Tests that all non-digit characters are stripped from the phone number."""
    customer = validated_customers[1]

    assert customer.phone == '6291605830'


def test_empty_optional_fields_is_none(validated_customers):
    """Verifies that optional fields that are empty in the CSV become None."""
    customer = validated_customers[0]

    assert customer.phone is None
    assert customer.cep is None
    assert customer.state is None
    assert customer.country is None


def test_just_headers_csv_returns_empty_list(customers_header_only_csv_data):
    """Tests that processing a CSV with only a header row returns an empty list."""
    csv_buffer = io.StringIO(customers_header_only_csv_data)
    adapter = MgtCustomersCsvAdapter(csv_buffer)

    processed_data = adapter.process()

    assert processed_data == []


def test_invalid_data_raises_error(customers_data_with_missing_required_field):
    """Tests that a ValueError is raised when a required field is missing from the data."""
    csv_buffer = io.StringIO(customers_data_with_missing_required_field)
    adapter = MgtCustomersCsvAdapter(csv_buffer)

    with pytest.raises(ValueError, match='Pydantic validation error'):
        adapter.process()
