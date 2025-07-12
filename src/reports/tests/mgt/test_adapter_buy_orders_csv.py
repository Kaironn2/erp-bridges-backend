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
        '414797776;969693;Rodrigo;Freitas;sarahmendes@carvalho.com;Atacado;594.603.817-66;30/01/2025 22:01:33;81 4959-3103;Entregue;TRACK456;5;R$ 9,81;R$ 13,23;cartão;R$ 493,35'  # noqa: E501
    )


@pytest.fixture
def header_only_csv_data() -> str:
    """return buy orders csv headers"""
    return 'Pedido #;ID do Pedido;Firstname;Lastname;Email;Grupo do Cliente;Número CPF/CNPJ;Comprado Em;Shipping Telephone;Status;Número do Rastreador;Qtd. Vendida;Frete;Desconto;Payment Type;Total da Venda\n'  # noqa: E501


@pytest.fixture
def invalid_format_csv_data() -> str:
    """return string with an invalid format"""
    return (
        'Pedido #;ID do Pedido;Firstname;Lastname;Email;Grupo do Cliente;Número CPF/CNPJ;Comprado Em;Shipping Telephone;Status;Número do Rastreador;Qtd. Vendida;Frete;Desconto;Payment Type;Total da Venda\n'  # noqa: E501
        '507943839;201414;Luiza;Correia;email-invalido;VIP;091.764.823-40;10-04-2025 22:01:33;(71) 6379-4026;Cancelado;TRACK123;1;R$ 23,24;R$ 0,00;boleto;R$ 85,46'  # noqa: E501
    )


def test_successful_processing(valid_csv_data):
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
    assert order1.customer.first_name == 'luiza'
    assert order1.customer.last_name == 'correia'
    assert order1.customer.email == 'luigi32@viana.br'
    assert order1.customer.cpf == '09176482340'
    assert order1.customer.phone == '7163794026'

    # mapping
    assert order1.payment_type == 'boleto bancário'

    # second order data
    assert order2.buy_order == "414797776"
    assert order2.status == 'entregue'
    assert order2.payment_type == 'cartão de crédito'
    assert order2.customer.first_name == 'rodrigo'


def test_file_not_found_raises_error():
    pass    # TODO


def test_invalid_data_raises_validation_error(invalid_format_csv_data):
    pass    # TODO


def test_empty_or_header_only_file_returns_empty_list(header_only_csv_data):
    pass    # TODO
