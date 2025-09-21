from typing import Dict

from django.db import transaction

from buy_order.models import PaymentType


class PaymentTypeRepository:
    def find_all_as_dict(self) -> Dict[str, PaymentType]:
        return {p.name: p for p in PaymentType.objects.all()}

    def filter_by_names(self, names: list[str]) -> list[PaymentType]:
        return list(PaymentType.objects.filter(name__in=names))

    def get_or_create(self, name: str) -> PaymentType:
        payment_type, created = PaymentType.objects.get_or_create(name=name)
        return payment_type

    @transaction.atomic
    def get_or_create_many_by_name(self, names: list[str]) -> dict[str, PaymentType]:
        objs = []
        for name in names:
            obj, _ = PaymentType.objects.get_or_create(name=name)
            objs.append(obj)
        return {obj.name: obj for obj in objs}
