from datetime import datetime
from decimal import Decimal
from typing import Optional, TypedDict

from django.db.models.query import QuerySet

from buy_order.models import BuyOrder, PaymentType, Status
from customer.models import Customer


class BuyOrderDataType(TypedDict):
    order_number: str
    customer: Customer
    payment_type: PaymentType
    status: Status
    order_id: str
    order_date: datetime
    shipping_amount: Decimal
    discount_amount: Decimal
    total_amount: Decimal
    sold_quantity: int


class BuyOrderRepository:
    def create(self, buy_order_data: BuyOrderDataType) -> BuyOrder:
        return BuyOrder.objects.create(**buy_order_data)

    def find_all(self) -> QuerySet[BuyOrder]:
        return BuyOrder.objects.all()

    def find_by_order_number(self, order_number: str) -> Optional[BuyOrder]:
        try:
            return BuyOrder.objects.get(order_number=order_number)
        except BuyOrder.DoesNotExist:
            return None

    def build(self, data: BuyOrderDataType) -> BuyOrder:
        return BuyOrder(**data)

    def bulk_create(self, orders: list[BuyOrder]) -> list[BuyOrder]:
        return list(
            BuyOrder.objects.bulk_create(
                orders,
                update_conflicts=True,
                update_fields=['status'],
                unique_fields=['order_number'],
            )
        )
