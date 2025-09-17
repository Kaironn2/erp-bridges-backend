from typing import Optional

import pandas as pd
from django.db import transaction

from core.ingestion.base_loader import BaseLoader
from buy_order.models import BuyOrder
from buy_order.repositories.buy_order_repository import BuyOrderRepository
from buy_order.repositories.payment_type_repository import PaymentTypeRepository
from buy_order.repositories.status_repository import StatusRepository
from customer.models import Customer
from customer.repositories.customer_repository import CustomerRepository
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
            self._process_customers()
            self._process_buy_orders()

    def _process_customers(self) -> None:
        emails = self.df['email'].unique().tolist()
        cpfs = self.df['cpf'].dropna().unique().tolist()

        existing_customers = Customer.objects.filter(email__in=emails) | Customer.objects.filter(
            cpf__in=cpfs
        )
        customers_by_email = {c.email: c for c in existing_customers}
        customers_by_cpf = {c.cpf: c for c in existing_customers if c.cpf}

        groups = self.customer_group_repo.filter_by_names(
            self.df['customer_group'].unique().tolist()
        )
        groups_by_name = {g.name: g for g in groups}

        new_customers, update_customers = [], []

        for _, row in self.df.iterrows():
            group = groups_by_name.get(
                row['customer_group']
            ) or self.customer_group_repo.get_or_create(row['customer_group'])

            customer = customers_by_email.get(row['email']) or customers_by_cpf.get(row['cpf'])
            if not customer:
                new_customers.append(
                    self.customer_repo.build({
                        'first_name': row['first_name'],
                        'last_name': row['last_name'],
                        'email': row['email'],
                        'cpf': row['cpf'],
                        'phone': row['phone'],
                        'last_order': row['order_date'],
                        'customer_group': group,
                    })
                )
            elif not customer.last_order or customer.last_order < row['order_date']:
                customer.last_order = row['order_date']
                customer.customer_group = group
                update_customers.append(customer)

        if new_customers:
            self.customer_repo.bulk_create(new_customers, ignore_conflicts=True)
        if update_customers:
            self.customer_repo.bulk_update(update_customers, ['last_order', 'customer_group'])

    def _buy_orders_mapping(self, order_numbers: list[str]) -> Optional[dict[str, BuyOrder]]:
        existing_orders = self.buy_order_repo.find_by_order_number(order_numbers)
        if existing_orders is None:
            return None
        return {order.order_number: order for order in existing_orders}

    def _process_buy_orders(self) -> None:
        customers = self.customer_repo.find_all()
        customers_by_email = {c.email: c for c in customers if c.email}
        customers_by_cpf = {c.cpf: c for c in customers if c.cpf}

        payments = self.payment_type_repo.filter_by_names(
            self.df['payment_type'].unique().tolist()
        )
        payments_by_name = {p.name: p for p in payments}

        statuses = self.status_repo.filter_by_names(self.df['status'].unique().tolist())
        statuses_by_name = {s.name: s for s in statuses}

        orders = []

        for _, row in self.df.iterrows():
            customer = customers_by_email.get(row['email']) or customers_by_cpf.get(row['cpf'])
            payment_type = payments_by_name.get(
                row['payment_type']
            ) or self.payment_type_repo.get_or_create(row['payment_type'])
            status = statuses_by_name.get(row['status']) or self.status_repo.get_or_create(
                row['status']
            )

            orders.append(
                BuyOrder(
                    order_number=row['order_number'],
                    customer=customer,
                    payment_type=payment_type,
                    status=status,
                    order_id=row['order_id'],
                    order_date=row['order_date'],
                    sold_quantity=row['sold_quantity'],
                    discount_amount=row['discount_amount'],
                    shipping_amount=row['shipping_amount'],
                    total_amount=row['total_amount'],
                )
            )

        if orders:
            self.buy_order_repo.bulk_create(orders)
