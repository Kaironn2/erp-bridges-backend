from typing import Dict

from mgt.models import BuyOrder, BuyOrderDetail


class BuyOrderDetailRepository:

    def update_or_create(self, buy_order: BuyOrder, buy_order_detail_data: Dict) -> BuyOrderDetail:
        buy_order_detail, _ = BuyOrderDetail.objects.update_or_create(
            buy_order=buy_order, defaults=buy_order_detail_data
        )
        return buy_order_detail
