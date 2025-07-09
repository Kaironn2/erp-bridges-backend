from __future__ import annotations

from datetime import datetime
from decimal import Decimal
from typing import Any, Dict, Optional

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
    shipping_amount: Decimal = Field(alias='Frete')
    discount: Decimal = Field(alias='Desconto')
    total_amount: Decimal = Field(alias='Total da Venda')

    customer: CustomerDataFromBuyOrder

    class Config:
        populate_by_name = True

    @classmethod
    def from_flat_dict(cls, record: Dict[str, Any]) -> BuyOrderReportData:
        main_data = {}
        customer_data = {}

        for field_name, field_info in cls.model_fields.items():
            if field_name == 'customer':
                continue
            source_column = field_info.alias or field_name
            main_data[field_name] = record.get(source_column)

        for field_name, field_info in CustomerDataFromBuyOrder.model_fields.items():
            source_column = field_info.alias or field_name
            customer_data[field_name] = record.get(source_column)

        structured_record = {**main_data, 'customer': customer_data}
        return cls.model_validate(structured_record)
