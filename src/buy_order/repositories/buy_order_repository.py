from typing import Optional, TypedDict

from django.db.models.query import QuerySet

from buy_order.models import BuyOrder
from customer.models import Customer


class BuyOrderDataType(TypedDict):
    order_number: str
    customer: Customer


class BuyOrderRepository:
    def find_all(self) -> QuerySet[BuyOrder]:
        return BuyOrder.objects.all()

    def find_by_order_number(self, order_number: list[str]) -> Optional[list[BuyOrder]]:
        return list(BuyOrder.objects.filter(order_number__in=order_number))

    def build(self, data: BuyOrderDataType) -> BuyOrder:
        return BuyOrder(**data)

    def get_or_create(self, buy_order_data: BuyOrderDataType) -> BuyOrder:
        order_number = buy_order_data.pop('order_number')
        buy_order, created = BuyOrder.objects.get_or_create(
            order_number=order_number, defaults=dict(buy_order_data)
        )
        return buy_order

    def bulk_create(self, orders: list[BuyOrder]) -> list[BuyOrder]:
        return list(
            BuyOrder.objects.bulk_create(
                orders,
                update_conflicts=True,
                update_fields=['status'],
                unique_fields=['order_number'],
            )
        )
