from decimal import Decimal
from datetime import datetime
from typing import TypedDict

from buy_order.models import BuyOrder, Company
from invoice.models import Invoice


class InvoiceDataType(TypedDict):
    buy_order: BuyOrder
    number: str
    access_key: str
    operation_nature: str
    cfop: str
    issue_date: datetime
    company: Company
    shipping_amount: Decimal
    total_amount: Decimal
    recipient_cpf: str
    recipient_name: str
    recipient_street: str
    recipient_street_number: str
    recipient_neighborhood: str
    recipient_city: str
    recipient_state: str
    recipient_zip_code: str
    recipient_country: str
    recipient_phone: str
    recipient_email: str


class InvoiceRepository:
    def build(self, data: InvoiceDataType) -> Invoice:
        return Invoice(**data)

    def bulk_create(self, invoices: list[Invoice]) -> list[Invoice]:
        return list(
            Invoice.objects.bulk_create(
                invoices, unique_fields=['access_key'], ignore_conflicts=True
            )
        )
