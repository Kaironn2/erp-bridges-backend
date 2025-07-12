from datetime import datetime
from decimal import Decimal
import io

import pytest

from mgt.schemas.buy_orders_report_schema import BuyOrderReportData
from reports.adapters.mgt.buy_orders_csv_adapter import MgtBuyOrdersCsvAdapter


@pytest.fixture
def valid_csv_data() -> str:
    """Retorna uma string multi-linhas com dados CSV válidos e complexos para testar todas as regras."""
    return (
        'Pedido #;ID do Pedido;Firstname;Lastname;Email;Grupo do Cliente;Número CPF/CNPJ;Comprado Em;Shipping Telephone;Status;Número do Rastreador;Qtd. Vendida;Frete;Desconto;Payment Type;Total da Venda\n'
        '507943839;201414;Luiza;Correia;luigi32@VIANA.br;VIP;091.764.823-40;10/04/2025 22:01:33;(71) 6379-4026;Cancelado;TRACK123;1;R$ 23,24;R$ 0,00;boleto;R$ 85,46\n'
        '414797776;969693;Rodrigo;Freitas;sarahmendes@carvalho.com;Atacado;594.603.817-66;30/01/2025 22:01:33;81 4959-3103;Entregue;TRACK456;5;R$ 9,81;R$ 13,23;cartão;R$ 493,35'
    )


@pytest.fixture
def header_only_csv_data() -> str:
    """Retorna um CSV contendo apenas o cabeçalho."""
    return 'Pedido #;ID do Pedido;Firstname;Lastname;Email;Grupo do Cliente;Número CPF/CNPJ;Comprado Em;Shipping Telephone;Status;Número do Rastreador;Qtd. Vendida;Frete;Desconto;Payment Type;Total da Venda\n'


@pytest.fixture
def invalid_format_csv_data() -> str:
    """Retorna um CSV com dados que falharão na validação do Pydantic (data e email)."""
    return (
        'Pedido #;ID do Pedido;Firstname;Lastname;Email;Grupo do Cliente;Número CPF/CNPJ;Comprado Em;Shipping Telephone;Status;Número do Rastreador;Qtd. Vendida;Frete;Desconto;Payment Type;Total da Venda\n'
        '507943839;201414;Luiza;Correia;email-invalido;VIP;091.764.823-40;10-04-2025 22:01:33;(71) 6379-4026;Cancelado;TRACK123;1;R$ 23,24;R$ 0,00;boleto;R$ 85,46'
    )


# --- Testes ---


def test_successful_processing(valid_csv_data):
    """
    Testa o 'caminho feliz': processa um CSV válido e verifica todas as transformações.
    """
    # Prepara o adapter usando a fixture com os dados válidos
    csv_buffer = io.StringIO(valid_csv_data)
    adapter = MgtBuyOrdersCsvAdapter(csv_buffer)

    # Executa o processo
    validated_data = adapter.process()

    # ---- Asserções (Verificações) ----

    # Verifica a quantidade e o tipo dos objetos retornados
    assert len(validated_data) == 2
    assert isinstance(validated_data[0], BuyOrderReportData)

    # Verifica o primeiro registro em detalhe
    first_order = validated_data[0]
    assert first_order.buy_order == '507943839'
    assert first_order.status == 'cancelado'  # Testando lowercase
    assert first_order.tracking_code == 'TRACK123'

    # Testando a limpeza de moeda e conversão para Decimal
    assert isinstance(first_order.shipping_amount, Decimal)
    assert first_order.shipping_amount == Decimal('23.24')
    assert first_order.discount == Decimal('0.00')

    # Testando a conversão de data
    assert isinstance(first_order.buy_order_date, datetime)
    assert first_order.buy_order_date == datetime(2025, 4, 10, 22, 1, 33)

    # Testando o objeto aninhado 'customer' e suas transformações
    assert isinstance(first_order.customer, BuyOrderReportData.customer.field_info.annotation)
    assert first_order.customer.first_name == 'luiza'  # Lowercase
    assert first_order.customer.email == 'luigi32@viana.br'  # Lowercase
    assert first_order.customer.cpf == '09176482340'  # Apenas dígitos
    assert first_order.customer.phone == '7163794026'  # Apenas dígitos

    # Testando a substituição de valores (mapping)
    assert first_order.payment_type == 'boleto bancário'

    # Verifica um campo do segundo registro para garantir a iteração
    second_order = validated_data[1]
    assert second_order.buy_order == '414797776'
    assert second_order.status == 'entregue'
    assert second_order.payment_type == 'cartão de crédito'
    assert second_order.customer.first_name == 'rodrigo'


def test_file_not_found_raises_error():
    """Verifica se um ValueError é levantado quando o arquivo não existe."""
    with pytest.raises(ValueError, match='Arquivo não encontrado'):
        MgtBuyOrdersCsvAdapter('caminho/para/arquivo/inexistente.csv')


def test_invalid_data_raises_validation_error(invalid_format_csv_data):
    """
    Verifica se dados que não passam na validação do Pydantic (após a limpeza)
    levantam um ValueError.
    """
    csv_buffer = io.StringIO(invalid_format_csv_data)
    adapter = MgtBuyOrdersCsvAdapter(csv_buffer)

    # O método process deve capturar a ValidationError do Pydantic e levantar um ValueError
    with pytest.raises(ValueError, match='Pydantic validation error'):
        adapter.process()


def test_empty_or_header_only_file_returns_empty_list(header_only_csv_data):
    """Verifica se um arquivo contendo apenas o cabeçalho retorna uma lista vazia."""
    csv_buffer = io.StringIO(header_only_csv_data)
    adapter = MgtBuyOrdersCsvAdapter(csv_buffer)

    validated_data = adapter.process()

    assert validated_data == []
