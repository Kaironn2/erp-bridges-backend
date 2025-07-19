import pytest
from rest_framework.test import APIClient


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def customers_valid_csv_byte_string() -> str:
    """Returns a multi-line string with valid customer report data."""
    csv_string = (
        '"Créditos / Vale Presentes",ID,Nome,E-mail,Grupo,Telefone,CEP,País,Estado,"Cliente Desde"\n'  # noqa: E501
        '"R$0,00",189117,"Júlya Viana",julyaviana23@gmail.com,Comum,,,,,"14/07/2025 11:04:50"\n'  # noqa: E501
        '"R$0,00",189111,"Sandra Rodrigues da Silva",sandraritasilva2064@gmail.com,Comum,"(62) 9160-5830",74911-110,Brasil,GO,"14/07/2025 10:43:22"\n'  # noqa: E501
        '"R$0,00",189099,"Karla karoline de Jesus cerqueira",karlla.fsa20@gmail.com,Comum," - ",44002-365,Brasil,BA,"14/07/2025 09:14:50"\n'  # noqa: E501
        '"R$0,00",189106,"MARIA HELENA RIBEIRO BRISTOTTI",m.lu.bristotti@gmail.com,Comum,,,,,"14/07/2025 10:01:53"\n'  # noqa: E501
    )

    return csv_string.encode('utf-8')
