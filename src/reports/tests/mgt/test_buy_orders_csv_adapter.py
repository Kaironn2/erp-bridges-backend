from datetime import datetime
from decimal import Decimal
import io

import pytest

from mgt.schemas.buy_orders_report_schema import BuyOrderReportData
from reports.adapters.mgt.buy_orders_csv_adapter import MgtBuyOrdersCsvAdapter


@pytest.fixture
def valid_csv_data() -> str:
    """return multi line string with valid data"""
    return (
        "Pedido #;ID do Pedido;Firstname;Lastname;Email;Grupo do Cliente;Número CPF/CNPJ;Comprado Em;Shipping Telephone;Status;Número do Rastreador;Qtd. Vendida;Frete;Desconto;Payment Type;Total da Venda\n"
        "507943839;201414;Luiza;Correia;luigi32@VIANA.br;VIP;091.764.823-40;10/04/2025 22:01:33;(71) 6379-4026;Cancelado;TRACK123;1;R$ 23,24;R$ 0,00;boleto;R$ 85,46\n"
        "414797776;969693;Rodrigo;Freitas;sarahmendes@carvalho.com;Atacado;594.603.817-66;30/01/2025 22:01:33;81 4959-3103;Entregue;TRACK456;5;R$ 9,81;R$ 13,23;cartão;R$ 493,35"
    )


@pytest.fixture
def header_only_csv_data() -> str:
    """return buy orders csv headers"""
    return "Pedido #;ID do Pedido;Firstname;Lastname;Email;Grupo do Cliente;Número CPF/CNPJ;Comprado Em;Shipping Telephone;Status;Número do Rastreador;Qtd. Vendida;Frete;Desconto;Payment Type;Total da Venda\n"


@pytest.fixture
def invalid_format_csv_data() -> str:
    """return string with an invalid format"""
    return (
        "Pedido #;ID do Pedido;Firstname;Lastname;Email;Grupo do Cliente;Número CPF/CNPJ;Comprado Em;Shipping Telephone;Status;Número do Rastreador;Qtd. Vendida;Frete;Desconto;Payment Type;Total da Venda\n"
        "507943839;201414;Luiza;Correia;email-invalido;VIP;091.764.823-40;10-04-2025 22:01:33;(71) 6379-4026;Cancelado;TRACK123;1;R$ 23,24;R$ 0,00;boleto;R$ 85,46"
    )


def test_successful_processing(valid_csv_data):
    csv_buffer = io.StringIO(valid_csv_data)
    adapter = MgtBuyOrdersCsvAdapter(csv_buffer)

    validated_data = adapter.process()

    validated_objects = 2
    assert len(validated_data) == validated_objects
