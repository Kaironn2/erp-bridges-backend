from collections.abc import Sequence
from datetime import datetime
from typing import Optional, Literal, TypedDict

from django.db.models import Q, QuerySet

from mgt.models import Customer, CustomerGroup


class GetByEmailOrCpfType(TypedDict):
    email: str
    cpf: str


class CustomerDataType(TypedDict, total=False):
    id: Optional[str]
    external_id: Optional[str]
    first_name: str
    last_name: str
    email: str
    cpf: Optional[str]
    phone: Optional[str]
    customer_group: CustomerGroup
    customer_since: Optional[datetime]
    postal_code: Optional[str]
    city: Optional[str]
    state: Optional[str]
    country: Optional[str]
    last_order: Optional[datetime]


CustomerUpdateFields = Literal['external_id', 'customer_since', 'last_order', 'customer_group']


class CustomerRepository:
    def find_all(self) -> QuerySet[Customer]:
        return Customer.objects.all()

    def build(self, data: CustomerDataType) -> Customer:
        return Customer(**data)

    def find_by_email_or_cpf(
        self, email: Optional[str] = None, cpf: Optional[str] = None
    ) -> Optional[Customer]:
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

    def create(self, customer_data: CustomerDataType) -> Customer:
        return Customer.objects.create(**customer_data)

    def update(self, customer: Customer, customer_data: CustomerDataType) -> Customer:
        for attr, value in customer_data.items():
            setattr(customer, attr, value)
        customer.save()
        return customer

    def upsert(self, customer_data: CustomerDataType) -> Customer:
        """
        Updates an existing customer or creates a new one based on the email.
        """
        email = customer_data.pop('email')
        customer, created = Customer.objects.update_or_create(
            email=email, defaults=dict(customer_data)
        )
        return customer

    def bulk_create(self, customers: list[Customer], ignore_conflicts: bool) -> list[Customer]:
        return Customer.objects.bulk_create(customers, ignore_conflicts=True)

    def bulk_update(
        self, customers: list[Customer], fields: Sequence[CustomerUpdateFields]
    ) -> None:
        Customer.objects.bulk_update(customers, fields)

    def bulk_upsert(self, customers: list[Customer]) -> None:
        Customer.objects.bulk_create(
            customers,
            batch_size=5000,
            update_conflicts=True,
            update_fields=[
                'cpf',
                'email',
                'first_name',
                'last_name',
                'phone',
                'last_order',
                'customer_group',
            ],
            unique_fields=['email'],
        )
