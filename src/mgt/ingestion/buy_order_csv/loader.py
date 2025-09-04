from typing import Any

import pandas as pd
from django.db import transaction

from core.ingestion.base_loader import BaseLoader
from mgt.repositories.buy_order_repository import BuyOrderRepository
from mgt.repositories.buy_order_detail_respository import BuyOrderDetailRepository
from mgt.repositories.customer_repository import CustomerRepository
from mgt.repositories.customer_group_repository import CustomerGroupRepository
from mgt.repositories.payment_type_repository import PaymentTypeRepository
from mgt.repositories.status_repository import StatusRepository


class BuyOrderCsvLoader(BaseLoader):
    def __init__(self, df: pd.DataFrame) -> None:
        self.df = df
        self.buy_order_repo = BuyOrderRepository()
        self.buy_order_detail_repo = BuyOrderDetailRepository()
        self.customer_repo = CustomerRepository()
        self.customer_group_repo = CustomerGroupRepository()
        self.payment_type_repo = PaymentTypeRepository()
        self.status_repo = StatusRepository()
        self.customers = []
        self.buy_orders = []
        self.buy_orders_details = []

    def load(self) -> None:
        with transaction.atomic():
            self._cached_data()
            self._build_data()
            self._upsert_data()

    def _upsert_data(self) -> None:
        self.customer_repo.bulk_upsert(self.customers)
        self.buy_order_repo.bulk_create(self.buy_orders, ignore_conflicts=True)
        self.buy_order_detail_repo.bulk_upsert(self.buy_orders_details)

    def _build_data(self) -> None:
        for _, row in self.df.iterrows():
            self._build_customers(row)
            self._build_buy_orders(row)
            self._build_buy_orders_details(row)

    def _build_customers(self, row: pd.Series[Any]) -> None:
        customer_group = self.customer_group_repo.get_or_create(row['customer_group'])

        customer = self.customer_by_email.get(row['email']) or self.customers_by_cpf.get(
            row['cpf']
        )

        if not customer or not customer.last_order or customer.last_order < row['order_date']:
            new_customer = self.customer_repo.build(
                cpf=row['cpf'],
                email=row['email'],
                first_name=row['first_name'],
                last_name=row['last_name'],
                phone=row['phone'],
                last_order=row['order_date'],
                customer_group=customer_group,
            )
            self.customer_by_email['email'] = new_customer
            self.customers_by_cpf['cpf'] = new_customer
            self.customers.append(new_customer)

    def _build_buy_orders(self, row: pd.Series[Any]) -> None:
        customer = self.customer_by_email.get(row['email']) or self.customers_by_cpf.get(
            row['cpf']
        )

        if not customer:
            return

        self.buy_orders.append(
            self.buy_order_repo.build(
                order_number=row['order_number'],
                customer=customer,
            )
        )

    def _build_buy_orders_details(self, row: pd.Series[Any]) -> None:
        buy_order = self.buy_order_repo.find_by_order_number(row['order_number'])
        payment_type = self.payment_type_repo.get_or_create(row['payment_type'])
        status = self.status_repo.get_or_create(row['status'])

        if not buy_order:
            return

        self.buy_orders_details.append(
            self.buy_order_detail_repo.build(
                buy_order=buy_order,
                order_external_id=row['order_external_id'],
                order_date=row['order_date'],
                payment_type=payment_type,
                tracking_code=row['tracking_code'],
                status=status,
                sold_quantity=row['sold_quantity'],
                shipping_amount=row['shipping_amount'],
                discount_amount=row['discount_amount'],
                total_amount=row['total_amount'],
            )
        )

    def _cached_data(self) -> None:
        self.all_customers = self.customer_repo.find_all()
        self.customer_by_email = {c.email: c for c in self.all_customers}
        self.customers_by_cpf = {c.cpf: c for c in self.all_customers}
