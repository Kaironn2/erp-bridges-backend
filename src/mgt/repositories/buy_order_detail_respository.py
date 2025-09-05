from datetime import datetime
from decimal import Decimal
from typing import List, Optional, TypedDict

from mgt.models import BuyOrder, BuyOrderDetail, PaymentType, Status


class BuyOrderDetailData(TypedDict):
    buy_order: BuyOrder
    order_external_id: str
    order_date: datetime
    payment_type: PaymentType
    tracking_code: Optional[str]
    status: Status
    sold_quantity: int
    shipping_amount: Decimal
    discount_amount: Decimal
    total_amount: Decimal


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

    def bulk_upsert(self, details: List[BuyOrderDetail]) -> None:
        BuyOrderDetail.objects.bulk_create(
            details,
            batch_size=5000,
            update_conflicts=True,
            update_fields=[
                'status',
                'tracking_code',
            ],
            unique_fields=['order_external_id'],
        )
