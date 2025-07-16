from typing import Optional

from django.db.models import Q

from mgt.models import Customer
from mgt.schemas.buy_orders_report_schema import CustomerDataFromBuyOrder
from mgt.schemas.customers_report_schema import CustomerReportData


class CustomerRepository:

    def _find_by_email_or_cpf(self, email: str, cpf: str) -> Optional[Customer]:
        """
        Finds a single customer by their email OR their CPF using a Q object.
        Returns the customer instance or None if not found.
        """
        query = Q()
        if email:
            query |= Q(email__iexact=email)
        if cpf:
            query |= Q(cpf=cpf)

        if not query:
            return None

        return Customer.objects.filter(query).first()

    def update_or_create(self, customer_schema: CustomerDataFromBuyOrder | CustomerReportData):
        update_data = customer_schema.model_dump(exclude_unset=True)
        email = update_data.pop('email')

        customer, created = Customer.objects.update_or_create(email=email, defaults=update_data)
        return customer
