from typing import Dict, List, Optional, TypedDict

from django.db.models import Q, QuerySet

from mgt.models import Customer


class GetByEmailOrCpfType(TypedDict):
    email: str
    cpf: str


class CustomerRepository:
    def find_all(self) -> QuerySet[Customer]:
        return Customer.objects.all()

    def build(self, **data) -> Customer:
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

    def create(self, customer_data: Dict) -> Customer:
        return Customer.objects.create(**customer_data)

    def update(self, customer: Customer, customer_data: Dict) -> Customer:
        for attr, value in customer_data.items():
            setattr(customer, attr, value)
        customer.save()
        return customer

    def bulk_upsert(self, customers: List[Customer]) -> None:
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
                'customer_group_id',
            ],
            unique_fields=['cpf']
        )
