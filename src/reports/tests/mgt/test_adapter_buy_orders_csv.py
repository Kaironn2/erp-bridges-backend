import io
from datetime import datetime
from decimal import Decimal

import pytest

from mgt.schemas.buy_orders_report_schema import BuyOrderReportData
from reports.adapters.mgt.buy_orders_csv_adapter import MgtBuyOrdersCsvAdapter


@pytest.fixture
def valid_csv_data() -> str:
    """return multi line string with valid data"""
    return (
        'Pedido #;ID do Pedido;Firstname;Lastname;Email;Grupo do Cliente;Número CPF/CNPJ;Comprado Em;Shipping Telephone;Status;Número do Rastreador;Qtd. Vendida;Frete;Desconto;Payment Type;Total da Venda\n'  # noqa: E501
        '507943839;201414;Luiza;Correia;luigi32@VIANA.br;VIP;091.764.823-40;10/04/2025 22:01:33;(71) 6379-4026;Cancelado;TRACK123;1;R$ 23,24;R$ 0,00;boleto;R$ 85,46\n'  # noqa: E501
        '414797776;969693;Rodrigo;Freitas;sarahmendes@carvalho.com;Atacado;594.603.817-66;30/01/2025 22:01:33; - ;Entregue;teste;5;R$ 9,81;R$ 13,23;cartão;R$ 493,35\n'  # noqa: E501
    )


@pytest.fixture
def header_only_csv_data() -> str:
    """return buy orders csv headers"""
    return 'Pedido #;ID do Pedido;Firstname;Lastname;Email;Grupo do Cliente;Número CPF/CNPJ;Comprado Em;Shipping Telephone;Status;Número do Rastreador;Qtd. Vendida;Frete;Desconto;Payment Type;Total da Venda\n'  # noqa: E501


@pytest.fixture
def data_with_missing_required_field() -> str:
    """
    Return csv with an empty mandatory field
    """
    return (
        'Pedido #;ID do Pedido;Firstname;Lastname;Email;Grupo do Cliente;Número CPF/CNPJ;Shipping Telephone;Status;Número do Rastreador;Qtd. Vendida;Frete;Desconto;Payment Type;Total da Venda\n'  # noqa: E501
        '507943839;201414;Luiza;Correia;email-valido@teste.com;VIP;091.764.823-40;(71) 6379-4026;Cancelado;TRACK123;1;R$ 23,24;R$ 0,00;boleto;R$ 85,46'  # noqa: E501
    )


def test_successful_processing(valid_csv_data):
    """
    Tests whether when calling the process method, all processes occur correctly:
    objects created len; object instance type; data cleaning;
    conversion of monetary values; conversion to datetime;
    columns to lower case; suboject customer created;

    Args:
        valid_csv_data (str): fixture with valid csv data
    """
    csv_buffer = io.StringIO(valid_csv_data)
    adapter = MgtBuyOrdersCsvAdapter(csv_buffer)

    validated_data = adapter.process()
    order1 = validated_data[0]
    order2 = validated_data[1]

    # objects len generated and if is correct instance
    validated_objects_len = 2
    assert len(validated_data) == validated_objects_len
    assert isinstance(validated_data[0], BuyOrderReportData)

    # validated order data
    assert order1.buy_order == '507943839'
    assert order1.status == 'cancelado'
    assert order1.tracking_code == 'TRACK123'

    # order currency conversion to decimal
    assert order1.shipping_amount == Decimal('23.24')
    assert order1.discount == Decimal('0.00')
    assert order1.total_amount == Decimal('85.46')

    # date conversion
    assert order1.buy_order_date == datetime(2025, 4, 10, 22, 1, 33)

    # customer data
    assert order1.first_name == 'luiza'
    assert order1.last_name == 'correia'
    assert order1.email == 'luigi32@viana.br'
    assert order1.cpf == '09176482340'
    assert order1.phone == '7163794026'

    # mapping
    assert order1.payment_type == 'boleto bancário'

    # second order data
    assert order2.buy_order == '414797776'
    assert order2.status == 'entregue'
    assert order2.payment_type == 'cartão de crédito'
    assert order2.first_name == 'rodrigo'


def test_empty_strings_converted_to_none(valid_csv_data):
    """Checks if empty strings are converted to None after cleaning process

    Args:
        valid_csv_data (_type_): fixture with valid csv data
    """
    csv_buffer = io.StringIO(valid_csv_data)
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


def test_invalid_data_raises_validation_error(data_with_missing_required_field):
    """
    Checks whether a ValueError from Pydantic ValidatioError when a field is missing

    Args:
        data_with_missing_required_field (str): fixture with data missing one field
    """
    csv_buffer = io.StringIO(data_with_missing_required_field)
    adapter = MgtBuyOrdersCsvAdapter(csv_buffer)

    with pytest.raises(ValueError, match='Pydantic validation error'):
        adapter.process()


def test_empty_or_header_only_file_returns_empty_list(header_only_csv_data):
    """
    tests whether an empty list is returned when csv has no data
    other than the headers

    Args:
        header_only_csv_data (_type_): empty data csv fixture, only headers
    """
    csv_buffer = io.StringIO(header_only_csv_data)
    adapter = MgtBuyOrdersCsvAdapter(csv_buffer)

    validated_data = adapter.process()

    assert validated_data == []
