import pandas as pd
from django.db import transaction

from core.ingestion.base_loader import BaseLoader
from mgt.models import BuyOrder, BuyOrderDetail, Customer
from mgt.repositories.buy_order_repository import BuyOrderDataType, BuyOrderRepository
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

    def load(self) -> None:
        with transaction.atomic():
            self._process_customers()
            self._process_buy_orders()
            self._process_buy_order_details()

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

    def _process_buy_orders(self) -> None:
        customers = self.customer_repo.find_all()
        customers_by_email = {c.email: c for c in customers if c.email}
        customers_by_cpf = {c.cpf: c for c in customers if c.cpf}

        new_orders = []
        for _, row in self.df.iterrows():
            customer = customers_by_email.get(row['email']) or customers_by_cpf.get(row['cpf'])
            if customer:
                new_order: BuyOrderDataType = {
                    'order_number': row['order_number'],
                    'customer': customer,
                }
                new_orders.append(self.buy_order_repo.build(data=new_order))

        if new_orders:
            self.buy_order_repo.bulk_create(new_orders, ignore_conflicts=True)

    def _process_buy_order_details(self) -> None:
        order_ids = self.df['order_external_id'].unique().tolist()
        existing_details = self.buy_order_detail_repo.find_by_external_ids(order_ids)
        details_by_ext = {d.order_external_id: d for d in existing_details}

        payments = self.payment_type_repo.filter_by_names(
            self.df['payment_type'].unique().tolist()
        )
        payments_by_name = {p.name: p for p in payments}

        statuses = self.status_repo.filter_by_names(self.df['status'].unique().tolist())
        statuses_by_name = {s.name: s for s in statuses}

        new_details, update_details = [], []

        for _, row in self.df.iterrows():
            payment_type = payments_by_name.get(
                row['payment_type']
            ) or self.payment_type_repo.get_or_create(row['payment_type'])
            status = statuses_by_name.get(row['status']) or self.status_repo.get_or_create(
                row['status']
            )

            existing = details_by_ext.get(row['order_external_id'])
            if not existing:
                buy_order = BuyOrder.objects.filter(order_number=row['order_number']).first()
                if buy_order:
                    new_details.append(
                        BuyOrderDetail(
                            buy_order=buy_order,
                            payment_type=payment_type,
                            status=status,
                            order_external_id=row['order_external_id'],
                            order_date=row['order_date'],
                            tracking_code=row['tracking_code'],
                            sold_quantity=row['sold_quantity'],
                            discount_amount=row['discount_amount'],
                            shipping_amount=row['shipping_amount'],
                            total_amount=row['total_amount'],
                        )
                    )
            else:
                existing.status = status
                existing.tracking_code = row['tracking_code']
                update_details.append(existing)

        if new_details:
            self.buy_order_detail_repo.bulk_create(new_details, ignore_conflicts=True)
        if update_details:
            self.buy_order_detail_repo.bulk_update(update_details, ['status', 'tracking_code'])
