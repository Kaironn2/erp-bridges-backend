from datetime import datetime
from decimal import Decimal
from typing import Optional

from pydantic import BaseModel, Field


class BuyOrderReportData(BaseModel):
    order_number: str = Field(alias='Pedido #')
    order_external_id: str = Field(alias='ID do Pedido')
    order_date: datetime = Field(alias='Comprado Em')
    status: str = Field(alias='Status')
    tracking_code: Optional[str] = Field(alias='Número do Rastreador')
    sold_quantity: int = Field(alias='Qtd. Vendida')
    payment_type: str = Field(alias='Payment Type')
    shipping_amount: Decimal = Field(alias='Frete')
    discount: Decimal = Field(alias='Desconto')
    total_amount: Decimal = Field(alias='Total da Venda')

    first_name: str = Field(alias='Firstname')
    last_name: str = Field(alias='Lastname')
    email: str = Field(alias='Email')
    customer_group: str = Field(alias='Grupo do Cliente')
    cpf: str = Field(alias='Número CPF/CNPJ')
    phone: Optional[str] = Field(alias='Shipping Telephone')

    class Config:
        populate_by_name = True
