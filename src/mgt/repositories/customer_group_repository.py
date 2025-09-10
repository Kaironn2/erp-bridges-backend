from typing import Dict

from mgt.models import CustomerGroup


class CustomerGroupRepository:
    def get_or_create(self, name: str) -> CustomerGroup:
        customer_group, created = CustomerGroup.objects.get_or_create(name=name)
        return customer_group

    def find_all_as_dict(self) -> Dict[str, CustomerGroup]:
        return {g.name: g for g in CustomerGroup.objects.all()}

    def filter_by_names(self, names: list[str]) -> list[CustomerGroup]:
        return list(CustomerGroup.objects.filter(name__in=names))
