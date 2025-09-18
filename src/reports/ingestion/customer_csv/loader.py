import pandas as pd
from django.db import transaction

from core.ingestion.base_loader import BaseLoader
from customer.repositories.customer_repository import CustomerRepository, CustomerDataType
from customer.repositories.customer_group_repository import CustomerGroupRepository

from customer.models import Customer


class CustomerCsvLoader(BaseLoader):
    def __init__(self, df: pd.DataFrame) -> None:
        self.df = df
        self.customer_repo = CustomerRepository()
        self.customer_group_repo = CustomerGroupRepository()
        self.customers_by_email = {}
        self.customer_groups = {}

    def load(self) -> None:
        with transaction.atomic():
            self._preload_customers()
            self._preload_customer_groups()

            new_customers = []
            updated_customers = []

            for _, row in self.df.iterrows():
                customer = self.customers_by_email.get(row['email'])

                if customer:
                    self._update_customer(customer, row)
                    updated_customers.append(customer)
                else:
                    new_customer = self._build_customer(row)
                    new_customers.append(new_customer)

            self.customer_repo.bulk_create(new_customers, ignore_conflicts=True)

            self.customer_repo.bulk_update(updated_customers, ['customer_since', 'external_id'])

    def _preload_customers(self):
        emails = self.df['email'].unique().tolist()
        self.customers_by_email = {
            c.email: c
            for c in Customer.objects.filter(email__in=emails).only(
                'id', 'email', 'external_id', 'customer_since'
            )
        }

    def _preload_customer_groups(self):
        names = self.df['customer_group'].unique().tolist()
        groups = self.customer_group_repo.filter_by_names(names)
        self.customer_groups = {g.name: g for g in groups}

    def _build_customer(self, row: pd.Series) -> Customer:
        customer_group = self.customer_groups.get(row['customer_group'])
        if not customer_group:
            customer_group = self.customer_group_repo.get_or_create(row['customer_group'])
            self.customer_groups[customer_group.name] = customer_group

        customer: CustomerDataType = {
            'first_name': row['first_name'],
            'last_name': row['last_name'],
            'email': row['email'],
            'phone': row['phone'],
            'postal_code': row['postal_code'],
            'customer_since': row['customer_since'],
            'state': row['state'],
            'country': row['country'],
            'customer_group': customer_group,
            'external_id': row['external_id'],
        }

        return self.customer_repo.build(customer)

    def _update_customer(self, customer: Customer, row: pd.Series) -> None:
        customer.external_id = row['external_id']
        customer.customer_since = row['customer_since']
