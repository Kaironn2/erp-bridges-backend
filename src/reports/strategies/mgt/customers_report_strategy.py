from typing import List

from mgt.models import Customer, CustomerGroup
from mgt.repositories.customer_group_repository import CustomerGroupRepository
from mgt.repositories.customer_repository import CustomerRepository
from mgt.schemas.customers_report_schema import CustomerReportData
from reports.adapters.mgt.customers_csv_adapter import MgtCustomersCsvAdapter
from reports.strategies.base_strategy import BaseReportStrategy


class MgtCustomersReportStrategy(BaseReportStrategy):
    def __init__(self, file_path_or_buffer):
        super().__init__(file_path_or_buffer)
        self.customer_repo = CustomerRepository()
        self.customer_group_repo = CustomerGroupRepository()

    def process(self):
        for v_customer in self.validated_customers:
            self.update_or_create_customer(v_customer)

    def get_or_create_customer_group(self, customer_group: str) -> CustomerGroup:
        return self.customer_group_repo.get_or_create(customer_group)

    def update_customer(
        self, customer: Customer, validated_customer: CustomerReportData
    ) -> Customer:
        customer_data = {
            'external_id': validated_customer.external_id,
            'state': validated_customer.state,
            'country': validated_customer.country,
            'customer_since': validated_customer.customer_since,
        }
        updated = False
        for key, value in customer_data.items():
            if getattr(customer, key, None) != value:
                setattr(customer, key, value)
                updated = True

        if updated:
            customer.save()

        return customer

    def update_or_create_customer(self, validated_customer: CustomerReportData) -> Customer:
        customer = self.customer_repo.find_by_email_or_cpf(validated_customer.email)
        customer_group = self.get_or_create_customer_group(validated_customer.customer_group)
        customer_data = {
            'external_id': validated_customer.external_id,
            'first_name': validated_customer.first_name,
            'last_name': validated_customer.last_name,
            'email': validated_customer.email,
            'customer_group': customer_group,
            'phone': validated_customer.phone,
            'postal_code': validated_customer.postal_code,
            'state': validated_customer.state,
            'country': validated_customer.country,
            'customer_since': validated_customer.customer_since,
        }

        if customer:
            if customer.last_order:
                return self.update_customer(customer, validated_customer)
            return self.customer_repo.update(customer, customer_data)

        return self.customer_repo.create(customer_data)

    @property
    def validated_customers(self) -> List[CustomerReportData]:
        adapter = MgtCustomersCsvAdapter(self.file)
        return adapter.process()
