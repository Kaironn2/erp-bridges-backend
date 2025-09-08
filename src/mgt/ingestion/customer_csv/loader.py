import pandas as pd
from django.db import transaction

from core.ingestion.base_loader import BaseLoader
from mgt.repositories.customer_repository import CustomerRepository, CustomerDataType
from mgt.repositories.customer_group_repository import CustomerGroupRepository

from mgt.models import Customer


class CustomerCsvLoader(BaseLoader):
    def __init__(self, df: pd.DataFrame) -> None:
        self.df = df
        self.customer_repo = CustomerRepository()
        self.customer_group_repo = CustomerGroupRepository()

    def load(self) -> None:
        with transaction.atomic():
            for _, row in self.df.iterrows():
                self._upsert_customer(row)

    def _upsert_customer(self, row: pd.Series) -> None:
        customer = self.customer_repo.find_by_email_or_cpf(email=row['email'])

        if customer:
            self._update_customer(customer, row)
            return

        self._create_customer(row)

    def _create_customer(self, row: pd.Series) -> None:
        customer_group = self.customer_group_repo.get_or_create(row['customer_group'])

        customer_data: CustomerDataType = {
            'first_name': row['first_name'],
            'last_name': row['last_name'],
            'email': row['email'],
            'phone': row['phone'],
            'customer_since': row['customer_since'],
            'state': row['state'],
            'country': row['country'],
            'customer_group': customer_group,
            'external_id': row['external_id'],
        }
        self.customer_repo.create(customer_data)

    def _update_customer(self, customer: Customer, row: pd.Series) -> None:
        customer_data: CustomerDataType = {
            'external_id': row['external_id'],
            'customer_since': row['customer_since'],
        }
        self.customer_repo.update(customer, customer_data)
