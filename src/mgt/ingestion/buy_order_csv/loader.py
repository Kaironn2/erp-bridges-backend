import pandas as pd
from django.db import transaction

from core.ingestion.base_loader import BaseLoader
from mgt.models import BuyOrder, Customer
from mgt.repositories.buy_order_repository import BuyOrderRepository, BuyOrderData
from mgt.repositories.buy_order_detail_respository import (
    BuyOrderDetailRepository,
    BuyOrderDetailData,
)
from mgt.repositories.customer_repository import CustomerRepository, CustomerDataType
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

    def load(self) -> None:
        with transaction.atomic():
            for _, row in self.df.iterrows():
                customer = self._upsert_customer(row)
                buy_order = self._create_buy_order(row, customer)
                self._upsert_buy_order_detail(row, buy_order)

    def _upsert_customer(self, row: pd.Series) -> Customer:
        customer_group = self.customer_group_repo.get_or_create(row['customer_group'])
        customer = self.customer_repo.find_by_email_or_cpf(row['email'], row['cpf'])

        customer_data: CustomerDataType = {
            'first_name': row['first_name'],
            'last_name': row['last_name'],
            'email': row['email'],
            'cpf': row['cpf'],
            'phone': row['phone'],
            'last_order': row['order_date'],
            'customer_group': customer_group,
        }

        if not customer:
            return self.customer_repo.create(customer_data)

        if not customer.last_order or customer.last_order < row['order_date']:
            return self.customer_repo.update(customer, customer_data)

        return customer

    def _create_buy_order(self, row: pd.Series, customer: Customer) -> BuyOrder:
        buy_order_data: BuyOrderData = {'order_number': row['order_number'], 'customer': customer}
        return self.buy_order_repo.get_or_create(buy_order_data)

    def _upsert_buy_order_detail(self, row: pd.Series, buy_order: BuyOrder) -> None:
        payment_type = self.payment_type_repo.get_or_create(row['payment_type'])
        status = self.status_repo.get_or_create(row['status'])

        if not buy_order:
            return

        buy_order_detail_data: BuyOrderDetailData = {
            'buy_order': buy_order,
            'payment_type': payment_type,
            'status': status,
            'order_external_id': row['order_external_id'],
            'order_date': row['order_date'],
            'tracking_code': row['tracking_code'],
            'sold_quantity': row['sold_quantity'],
            'discount_amount': row['discount_amount'],
            'shipping_amount': row['shipping_amount'],
            'total_amount': row['total_amount'],
        }

        self.buy_order_detail_repo.upsert(buy_order_detail_data)
