from datetime import datetime
from typing import TypedDict


from buy_order.models import BuyOrder, EcsBuyOrder
from company.models import Company


class EcsBuyOrderDataType(TypedDict):
    buy_order: BuyOrder
    ecs_order_number: str
    ecs_order_id: str
    payment_date: datetime
    coupon: str
    company: Company
    deadline_days: int
    ecs_carrier: str
    recipient_name: str
    recipient_zip_code: str
    recipient_city: str
    recipient_state: str
    ecs_delivery_date: datetime


class EcsBuyOrderRepository:
    def upsert(self, ecs_buy_order_data: EcsBuyOrderDataType) -> EcsBuyOrder:
        data = dict(ecs_buy_order_data)
        ecs_order_id = data.pop('ecs_order_id')

        obj, _ = EcsBuyOrder.objects.update_or_create(
            ecs_order_id=ecs_order_id,
            defaults=dict(ecs_buy_order_data),
        )
        return obj
