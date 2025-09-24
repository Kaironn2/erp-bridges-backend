from decimal import Decimal
from datetime import datetime
from typing import TypedDict

from buy_order.models import BuyOrder, Company
from invoice.models import Invoice


class InvoiceDataType(TypedDict):
    buy_order: BuyOrder
    access_key: str
    operation_nature: str
    cfop: str
    issue_date: datetime
    company: Company
    shipping_amount: Decimal
    total_amount: Decimal
    cpf: str
    name: str
    street: str
    number: str
    neighborhood: str
    city: str
    state: str
    zip_code: str
    country: str
    phone: str
    email: str


class InvoiceRepository:
    def build(self, data: InvoiceDataType) -> Invoice:
        return Invoice(**data)

    def bulk_create(self, invoices: list[Invoice]) -> list[Invoice]:
        return list(
            Invoice.objects.bulk_create(
                invoices, unique_fields=['access_key'], ignore_conflicts=True
            )
        )
