import pandas as pd
from django.db import transaction

from core.ingestion.base_loader import BaseLoader
from buy_order.repositories.buy_order_repository import BuyOrderRepository, BuyOrderDataType
from buy_order.repositories.payment_type_repository import PaymentTypeRepository
from buy_order.repositories.status_repository import StatusRepository
from customer.repositories.customer_repository import CustomerRepository, CustomerDataType
from customer.repositories.customer_group_repository import CustomerGroupRepository


class BuyOrderCsvLoader(BaseLoader):
    def __init__(self, df: pd.DataFrame) -> None:
        self.df = df
        self.buy_order_repo = BuyOrderRepository()
        self.customer_repo = CustomerRepository()
        self.customer_group_repo = CustomerGroupRepository()
        self.payment_type_repo = PaymentTypeRepository()
        self.status_repo = StatusRepository()

    def load(self) -> None:
        with transaction.atomic():
            for _, row in self.df.iterrows():
                self._upsert_customer(row)
                self._upser_buy_order(row)

    def _upsert_customer(self, row: pd.Series) -> None:
        group = self.customer_group_repo.get_or_create(row.customer_group)
        customer = self.customer_repo.find_by_email_or_cpf(row.email, row.cpf)

        customer_data: CustomerDataType = {
            'first_name': row.first_name,
            'last_name': row.last_name,
            'email': row.email,
            'cpf': row.cpf,
            'phone': row.phone,
            'last_order': row.order_date,
            'customer_group': group,
        }

        if not customer:
            self.customer_repo.create(customer_data)
            return

        elif not customer.last_order or customer.last_order < row['order_date']:
            self.customer_repo.update(customer, customer_data)

    def _upser_buy_order(self, row: pd.Series) -> None:
        buy_order = self.buy_order_repo.find_by_order_number(row.order_number)
        status = self.status_repo.get_or_create(row.status)

        if buy_order:
            buy_order.status = status
            buy_order.save()
            return

        customer = self.customer_repo.find_by_email_or_cpf(email=row.email)
        payment_type = self.payment_type_repo.get_or_create(row.payment_type)

        if not customer or not status or not payment_type:
            return

        buy_order_data: BuyOrderDataType = {
            'order_number': row.order_number,
            'customer': customer,
            'payment_type': payment_type,
            'status': status,
            'order_id': row.order_id,
            'order_date': row.order_date,
            'sold_quantity': row.sold_quantity,
            'discount_amount': row.discount_amount,
            'shipping_amount': row.shipping_amount,
            'total_amount': row.total_amount,
        }

        self.buy_order_repo.create(buy_order_data)
