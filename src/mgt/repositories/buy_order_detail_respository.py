from collections.abc import Sequence
from datetime import datetime
from decimal import Decimal
from typing import Literal, TypedDict

from mgt.models import BuyOrder, BuyOrderDetail, PaymentType, Status


class BuyOrderDetailData(TypedDict):
    buy_order: BuyOrder
    order_external_id: str
    order_date: datetime
    payment_type: PaymentType
    status: Status
    sold_quantity: int
    shipping_amount: Decimal
    discount_amount: Decimal
    total_amount: Decimal


BuyOrderDetailUpdateFields = Literal['status']


class BuyOrderDetailRepository:
    def build(self, **data) -> BuyOrderDetail:
        return BuyOrderDetail(**data)

    def upsert(self, buy_order_detail_data: BuyOrderDetailData) -> BuyOrderDetail:
        buy_order = buy_order_detail_data.pop('buy_order')
        buy_order_detail, _ = BuyOrderDetail.objects.update_or_create(
            buy_order=buy_order,
            defaults=dict(buy_order_detail_data),
        )
        return buy_order_detail

    def bulk_create(
        self, orders_details: list[BuyOrderDetail], ignore_conflicts: bool
    ) -> list[BuyOrderDetail]:
        return BuyOrderDetail.objects.bulk_create(
            orders_details, ignore_conflicts=ignore_conflicts
        )

    def bulk_update(
        self, orders_details: list[BuyOrderDetail], fields: Sequence[BuyOrderDetailUpdateFields]
    ) -> None:
        BuyOrderDetail.objects.bulk_update(orders_details, fields)

    def find_by_external_ids(self, external_ids: list[str]) -> list[BuyOrderDetail]:
        return list(BuyOrderDetail.objects.filter(order_external_id__in=external_ids))
