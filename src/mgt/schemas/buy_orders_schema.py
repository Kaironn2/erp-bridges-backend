from datetime import datetime
from decimal import Decimal
from typing import Optional

from pydantic import BaseModel, Field


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
