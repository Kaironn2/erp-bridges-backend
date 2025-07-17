from mgt.models import BuyOrder, Customer


class BuyOrderRepository:

    def get_or_create(self, order_number: str, customer: Customer) -> BuyOrder:
        buy_order, created = BuyOrder.objects.get_or_create(
            order_number=order_number, defaults={'customer': customer}
        )
        return buy_order
