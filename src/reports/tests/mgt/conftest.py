import io
from typing import List

import pytest

from mgt.schemas.buy_orders_report_schema import BuyOrderReportData
from mgt.schemas.customers_report_schema import CustomerReportData
from reports.adapters.mgt.buy_orders_csv_adapter import MgtBuyOrdersCsvAdapter
from reports.adapters.mgt.customers_csv_adapter import MgtCustomersCsvAdapter


@pytest.fixture
def buy_orders_valid_csv_data() -> str:
    """return multi line string with valid buy orders data"""
    return (
        'Pedido #;ID do Pedido;Firstname;Lastname;Email;Grupo do Cliente;Número CPF/CNPJ;Comprado Em;Shipping Telephone;Status;Número do Rastreador;Qtd. Vendida;Frete;Desconto;Payment Type;Total da Venda\n'  # noqa: E501
        '507943839;201414;Luiza;Correia;luigi32@VIANA.br;VIP;091.764.823-40;10/04/2025 22:01:33;(71) 6379-4026;Cancelado;TRACK123;1;R$ 23,24;R$ 0,00;boleto;R$ 85,46\n'  # noqa: E501
        '414797776;969693;Rodrigo;Freitas;sarahmendes@carvalho.com;Atacado;594.603.817-66;30/01/2025 22:01:33; - ;Entregue;teste;5;R$ 9,81;R$ 13,23;cartão;R$ 493,35\n'  # noqa: E501
    )


@pytest.fixture
def validated_buy_orders(buy_orders_valid_csv_data) -> List[BuyOrderReportData]:
    csv_buffer = io.StringIO(buy_orders_valid_csv_data)
    adapter = MgtBuyOrdersCsvAdapter(csv_buffer)

    return adapter.process()


@pytest.fixture
def buy_orders_header_only_csv_data() -> str:
    """return buy orders csv headers"""
    return 'Pedido #;ID do Pedido;Firstname;Lastname;Email;Grupo do Cliente;Número CPF/CNPJ;Comprado Em;Shipping Telephone;Status;Número do Rastreador;Qtd. Vendida;Frete;Desconto;Payment Type;Total da Venda\n'  # noqa: E501


@pytest.fixture
def buy_orders_data_with_missing_required_field() -> str:
    """
    Return csv with an empty mandatory field
    """
    return (
        'Pedido #;ID do Pedido;Firstname;Lastname;Email;Grupo do Cliente;Número CPF/CNPJ;Shipping Telephone;Status;Número do Rastreador;Qtd. Vendida;Frete;Desconto;Payment Type;Total da Venda\n'  # noqa: E501
        '507943839;201414;Luiza;Correia;email-valido@teste.com;VIP;091.764.823-40;(71) 6379-4026;Cancelado;TRACK123;1;R$ 23,24;R$ 0,00;boleto;R$ 85,46'  # noqa: E501
    )


@pytest.fixture
def customers_valid_csv_data() -> str:
    """Returns a multi-line string with valid customer report data."""
    return (
        '"Créditos / Vale Presentes",ID,Nome,E-mail,Grupo,Telefone,CEP,País,Estado,"Cliente Desde"\n'  # noqa: E501
        '"R$0,00",189117,"Júlya Viana",julyaviana23@gmail.com,Comum,,,,,"14/07/2025 11:04:50"\n'  # noqa: E501
        '"R$0,00",189111,"Sandra Rodrigues da Silva",sandraritasilva2064@gmail.com,Comum,"(62) 9160-5830",74911-110,Brasil,GO,"14/07/2025 10:43:22"\n'  # noqa: E501
        '"R$0,00",189099,"Karla karoline de Jesus cerqueira",karlla.fsa20@gmail.com,Comum," - ",44002-365,Brasil,BA,"14/07/2025 09:14:50"\n'  # noqa: E501
        '"R$0,00",189106,"MARIA HELENA RIBEIRO BRISTOTTI",m.lu.bristotti@gmail.com,Comum,,,,,"14/07/2025 10:01:53"\n'  # noqa: E501
    )


@pytest.fixture
def validated_customers(customers_valid_csv_data) -> List[CustomerReportData]:
    csv_buffer = io.StringIO(customers_valid_csv_data)
    adapter = MgtCustomersCsvAdapter(csv_buffer)

    return adapter.process()


@pytest.fixture
def customers_header_only_csv_data() -> str:
    """Returns the headers for the customer report CSV."""
    return '"Créditos / Vale Presentes",ID,Nome,E-mail,Grupo,Telefone,CEP,País,Estado,"Cliente Desde"\n'  # noqa: E501


@pytest.fixture
def customers_data_with_missing_required_field() -> str:
    """Returns a CSV row with a required field (Nome) missing."""
    return (
        '"Créditos / Vale Presentes,ID,Nome,E-mail,Grupo,Telefone,CEP,País,Estado,"Cliente Desde"\n'  # noqa: E501
        '"R$0,00",189117,,julyaviana23@gmail.com,Comum,,,,,"14/07/2025 11:04:50"\n'
    )
