from mgt.repositories.customer_repository import CustomerRepository
from reports.strategies.base_strategy import BaseReportStrategy


class MgtCustomersReportStrategy(BaseReportStrategy):
    def __init__(self, file_path_or_buffer):
        super().__init__(file_path_or_buffer)
        self.customer_repo = CustomerRepository()

    def process(self):
        pass
