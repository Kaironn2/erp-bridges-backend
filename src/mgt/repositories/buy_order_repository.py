from typing import List, Optional, TypedDict

from django.db.models.query import QuerySet

from mgt.models import BuyOrder, Customer


class BuyOrderData(TypedDict):
    order_number: str
    customer: Customer


class BuyOrderRepository:
    def find_all(self) -> QuerySet[BuyOrder]:
        return BuyOrder.objects.all()

    def find_by_order_number(self, order_number: str) -> Optional[BuyOrder]:
        return BuyOrder.objects.filter(order_number=order_number).first()

    def build(self, **data) -> BuyOrder:
        return BuyOrder(**data)

    def get_or_create(self, buy_order_data: BuyOrderData) -> BuyOrder:
        order_number = buy_order_data.pop('order_number')
        buy_order, created = BuyOrder.objects.get_or_create(
            order_number=order_number, defaults=dict(buy_order_data)
        )
        return buy_order

    def bulk_create(self, orders: List[BuyOrder], ignore_conflicts: bool = True) -> None:
        BuyOrder.objects.bulk_create(orders, batch_size=5000, ignore_conflicts=ignore_conflicts)

    def bulk_upsert(self, orders: List[BuyOrder]) -> None:
        BuyOrder.objects.bulk_create(
            orders,
            batch_size=5000,
            update_conflicts=True,
            update_fields=['order_date', 'customer_id'],
        )
