from typing import Dict, List

from mgt.models import BuyOrder, BuyOrderDetail


class BuyOrderDetailRepository:
    def build(self, **data) -> BuyOrderDetail:
        return BuyOrderDetail(**data)

    def update_or_create(self, buy_order: BuyOrder, buy_order_detail_data: Dict) -> BuyOrderDetail:
        buy_order_detail, _ = BuyOrderDetail.objects.update_or_create(
            buy_order=buy_order, defaults=buy_order_detail_data
        )
        return buy_order_detail

    def bulk_upsert(self, details: List[BuyOrderDetail]) -> None:
        BuyOrderDetail.objects.bulk_create(
            details,
            batch_size=5000,
            update_conflicts=True,
            update_fields=[
                "status",
                "tracking_code",
            ],
            unique_fields=["order_external_id"],
        )
