import io
from typing import List

import pytest

from mgt.schemas.customers_report_schema import CustomerReportData
from reports.adapters.mgt.customers_csv_adapter import MgtCustomersCsvAdapter


@pytest.fixture
def valid_csv_data() -> str:
    """Returns a multi-line string with valid customer report data."""
    return (
        '"Créditos / Vale Presentes",ID,Nome,E-mail,Grupo,Telefone,CEP,País,Estado,"Cliente Desde"\n'  # noqa: E501
        '"R$0,00",189117,"Júlya Viana",julyaviana23@gmail.com,Comum,,,,,"14/07/2025 11:04:50"\n'  # noqa: E501
        '"R$0,00",189111,"Sandra Rodrigues da Silva",sandraritasilva2064@gmail.com,Comum,"(62) 9160-5830",74911-110,Brasil,GO,"14/07/2025 10:43:22"\n'  # noqa: E501
        '"R$0,00",189099,"Karla karoline de Jesus cerqueira",karlla.fsa20@gmail.com,Comum," - ",44002-365,Brasil,BA,"14/07/2025 09:14:50"\n'  # noqa: E501
        '"R$0,00",189106,"MARIA HELENA RIBEIRO BRISTOTTI",m.lu.bristotti@gmail.com,Comum,,,,,"14/07/2025 10:01:53"\n'  # noqa: E501
    )


@pytest.fixture
def validated_customers(valid_csv_data) -> List[CustomerReportData]:
    csv_buffer = io.StringIO(valid_csv_data)
    adapter = MgtCustomersCsvAdapter(csv_buffer)

    return adapter.process()


@pytest.fixture
def header_only_csv_data() -> str:
    """Returns the headers for the customer report CSV."""
    return '"Créditos / Vale Presentes",ID,Nome,E-mail,Grupo,Telefone,CEP,País,Estado,"Cliente Desde"\n'  # noqa: E501


@pytest.fixture
def data_with_missing_required_field() -> str:
    """Returns a CSV row with a required field (Nome) missing."""
    return (
        '"Créditos / Vale Presentes",ID,Nome,E-mail,Grupo,Telefone,CEP,País,Estado,"Cliente Desde"\n'  # noqa: E501
        '"R$0,00",189117,,julyaviana23@gmail.com,Comum,,,,,"14/07/2025 11:04:50"\n'
    )


def test_successful_processing(valid_csv_data):
    csv_buffer = io.StringIO(valid_csv_data)
    adapter = MgtCustomersCsvAdapter(csv_buffer)

    validated_data = adapter.process()

    customers_len = 4
    assert len(validated_data) == customers_len
    assert isinstance(validated_data[0], CustomerReportData)


def test_columns_split(validated_customers):
    customer1 = validated_customers[0]

    assert customer1.first_name == 'júlya'
    assert customer1.last_name == 'viana'
