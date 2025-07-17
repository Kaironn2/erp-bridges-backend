from mgt.models import CustomerGroup


class CustomerGroupRepository:

    def get_or_create(self, name: str) -> CustomerGroup:
        customer_group, created = CustomerGroup.objects.get_or_create(name=name)
        return customer_group
