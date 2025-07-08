from datetime import datetime
from typing import Optional

from pydantic import BaseModel, EmailStr, Field


class CustomerDataFromBuyOrder(BaseModel):
    first_name: str = Field(alias='Firstname')
    last_name: str = Field(alias='Lastname')
    email: EmailStr = Field(alias='Email')
    customer_group: Optional[str] = Field(alias='Grupo do Cliente')
    cpf: str = Field(alias='Número CPF/CNPJ')
    phone: Optional[str] = Field(alias='Shipping Telephone')


class BuyOrderReportData(BaseModel):
    buy_order: str = Field(alias='Pedido #')
    buy_order_external_id: str = Field(alias='ID do Pedido')
    buy_order_date: datetime = Field(alias='Comprado Em')
    status: str = Field(alias='Status')
    tracking_code: Optional[str] = Field(alias='Número do Rastreador')
    sold_quantity: int = Field(alias='Qtd. Vendida')
    payment_type: str = Field(alias='Payment Type')
    shipping_amount: float = Field(alias='Frete')
    discount: float = Field(alias='Desconto')
    total_amount: float = Field(alias='Total da Venda')

    customer: CustomerDataFromBuyOrder

    class Config:
        allow_population_by_field_name = True
