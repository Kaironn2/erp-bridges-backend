from typing import Dict, Optional

from django.db.models import Q

from mgt.models import Customer


class CustomerRepository:

    def find_by_email_or_cpf(self, email: str = None, cpf: str = None) -> Optional[Customer]:
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

    def create(self, customer_data: Dict) -> Customer:
        return Customer.objects.create(**customer_data)

    def update(self, customer: Customer, customer_data: Dict) -> Customer:
        for attr, value in customer_data.items():
            setattr(customer, attr, value)
        customer.save()
        return customer
