from typing import Optional, TypedDict

from django.db.models.query import QuerySet

from mgt.models import BuyOrder, Customer


class BuyOrderDataType(TypedDict):
    order_number: str
    customer: Customer


class BuyOrderRepository:
    def find_all(self) -> QuerySet[BuyOrder]:
        return BuyOrder.objects.all()

    def find_by_order_number(self, order_number: str) -> Optional[BuyOrder]:
        return BuyOrder.objects.filter(order_number=order_number).first()

    def build(self, data: BuyOrderDataType) -> BuyOrder:
        return BuyOrder(**data)

    def get_or_create(self, buy_order_data: BuyOrderDataType) -> BuyOrder:
        order_number = buy_order_data.pop('order_number')
        buy_order, created = BuyOrder.objects.get_or_create(
            order_number=order_number, defaults=dict(buy_order_data)
        )
        return buy_order

    def bulk_create(self, orders: list[BuyOrder], ignore_conflicts: bool = True) -> list[BuyOrder]:
        return list(BuyOrder.objects.bulk_create(orders, ignore_conflicts=ignore_conflicts))
