from typing import Dict
from mgt.models import PaymentType


class PaymentTypeRepository:
    def find_all_as_dict(self) -> Dict[str, PaymentType]:
        return {p.name: p for p in PaymentType.objects.all()}

    def get_or_create(self, name: str) -> PaymentType:
        payment_type, created = PaymentType.objects.get_or_create(name=name)
        return payment_type
