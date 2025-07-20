from typing import List

from mgt.models import BuyOrder, BuyOrderDetail, Customer
from mgt.repositories.buy_order_detail_respository import BuyOrderDetailRepository
from mgt.repositories.buy_order_repository import BuyOrderRepository
from mgt.repositories.customer_group_repository import CustomerGroupRepository
from mgt.repositories.customer_repository import CustomerRepository
from mgt.repositories.payment_type_repository import PaymentTypeRepository
from mgt.repositories.status_repository import StatusRepository
from mgt.schemas.buy_orders_report_schema import BuyOrderReportData
from reports.adapters.mgt.buy_orders_csv_adapter import MgtBuyOrdersCsvAdapter
from reports.strategies.base_strategy import BaseReportStrategy


class MgtBuyOrdersReportStrategy(BaseReportStrategy):
    def __init__(self, file_path_or_buffer):
        super().__init__(file_path_or_buffer)
        self.buy_orders_repo = BuyOrderRepository()
        self.buy_orders_detail_repo = BuyOrderDetailRepository()
        self.customer_repo = CustomerRepository()
        self.customer_group_repo = CustomerGroupRepository()
        self.payment_type_repo = PaymentTypeRepository()
        self.status_repo = StatusRepository()

    def process(self):
        for order in self.validated_orders:
            customer = self.get_create_or_update_customer(order)
            buy_order = self.get_or_create_buy_order(order.order_number, customer)
            self.update_or_create_buy_order_detail(buy_order, order)

    def get_create_or_update_customer(self, order: BuyOrderReportData) -> Customer:
        customer = self.customer_repo.find_by_email_or_cpf(order.email, order.cpf)
        customer_group = self.customer_group_repo.get_or_create(order.customer_group)
        customer_data = {
            'first_name': order.first_name,
            'last_name': order.last_name,
            'email': order.email,
            'customer_group': customer_group,
            'cpf': order.cpf,
            'phone': order.phone,
            'last_order': order.order_date,
        }

        if customer:
            if not customer.last_order or order.order_date > customer.last_order:
                return self.customer_repo.update(customer, customer_data)
            return customer

        return self.customer_repo.create(customer_data)

    def get_or_create_buy_order(self, order_number: str, customer: Customer) -> BuyOrder:
        return self.buy_orders_repo.get_or_create(order_number, customer)

    def update_or_create_buy_order_detail(
        self, buy_order: BuyOrder, order: BuyOrderReportData
    ) -> BuyOrderDetail:
        payment_type = self.payment_type_repo.get_or_create(order.payment_type)
        status = self.status_repo.get_or_create(order.status)
        buy_order_detail_data = {
            'order_external_id': order.order_external_id,
            'order_date': order.order_date,
            'status': status,
            'tracking_code': order.tracking_code,
            'sold_quantity': order.sold_quantity,
            'payment_type': payment_type,
            'shipping_amount': order.shipping_amount,
            'discount_amount': order.discount,
            'total_amount': order.total_amount
        }
        return self.buy_orders_detail_repo.update_or_create(buy_order, buy_order_detail_data)

    @property
    def validated_orders(self) -> List[BuyOrderReportData]:
        adapter = MgtBuyOrdersCsvAdapter(self.file)
        return adapter.process()
