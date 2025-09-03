from typing import List

from django.db.models.query import QuerySet

from mgt.models import BuyOrder, Customer


class BuyOrderRepository:
    def find_all(self) -> QuerySet[BuyOrder]:
        return BuyOrder.objects.all()

    def build(self, **data) -> BuyOrder:
        return BuyOrder(**data)

    def get_or_create(self, order_number: str, customer: Customer) -> BuyOrder:
        buy_order, created = BuyOrder.objects.get_or_create(
            order_number=order_number, defaults={"customer": customer}
        )
        return buy_order

    def bulk_create_ignore_conflicts(
        self, orders: List[BuyOrder], ignore_conflicts: bool = True
    ) -> None:
        BuyOrder.objects.bulk_create(orders, batch_size=5000, ignore_conflicts=ignore_conflicts)

    def bulk_upsert(self, orders: List[BuyOrder]) -> None:
        BuyOrder.objects.bulk_create(
            orders,
            batch_size=5000,
            update_conflicts=True,
            update_fields=["order_date", "customer_id"],
        )
