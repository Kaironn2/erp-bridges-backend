import pandas as pd
from django.db import transaction

from core.ingestion.base_loader import BaseLoader
from buy_order.repositories.buy_order_repository import BuyOrderRepository
from company.repositories.company_repository import CompanyRepository
from invoice.repositories.invoice_repository import InvoiceRepository, InvoiceDataType


class InvoiceXmlLoader(BaseLoader):
    def __init__(self, df: pd.DataFrame) -> None:
        self.df = df
        self.buy_orders_repo = BuyOrderRepository()
        self.company_repo = CompanyRepository()
        self.invoice_repo = InvoiceRepository()

    def load(self) -> None:
        self._get_buy_orders_mapping()

        with transaction.atomic():
            ...

    def _get_buy_orders_mapping(self):
        order_numbers = list(self.df['order_number'].unique())
        buy_orders = self.buy_orders_repo.find_by_order_numbers(order_numbers)
        self.buy_orders = {bo.order_number: bo for bo in buy_orders}

    def _build_invoice(self, row: pd.Series):
        buy_order = self.buy_orders.get(row.order_number)
        company = self.company_repo.get_or_create(row.cnpj)

        invoice: InvoiceDataType = {
            'access_key': row.access_key,
            'number': row.number,
            'buy_order': buy_order,
            'company': company,
            'cfop': row.cfop,
            'operation_nature': row.operation_nature,
            'issue_date': row.issue_date,
        }
