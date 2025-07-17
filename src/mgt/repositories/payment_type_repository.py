from mgt.models import PaymentType


class PaymentTypeRepository:

    def get_or_create(self, name: str) -> PaymentType:
        payment_type, created = PaymentType.objects.get_or_create(name=name)
        return payment_type
