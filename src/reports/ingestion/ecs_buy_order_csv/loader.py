import pandas as pd
from django.db import transaction

from core.ingestion.base_loader import BaseLoader
from buy_order.repositories.buy_order_repository import BuyOrderRepository
from buy_order.repositories.ecs_buy_order_repository import (
    EcsBuyOrderDataType,
    EcsBuyOrderRepository,
)
from company.repositories.company_repository import CompanyRepository, CompanyDataType


class EcsBuyOrderCsvLoader(BaseLoader):
    def __init__(self, df: pd.DataFrame) -> None:
        self.df = df
        self.buy_order_repo = BuyOrderRepository()
        self.company_repo = CompanyRepository()
        self.ecs_buy_order_repo = EcsBuyOrderRepository()

    def load(self) -> None:
        with transaction.atomic():
            for _, row in self.df.iterrows():
                self._upsert_ecs_buy_order(row)

    def _upsert_ecs_buy_order(self, row: pd.Series) -> None:
        buy_order = self.buy_order_repo.find_by_order_number(row.order_number)

        company_data: CompanyDataType = {'cnpj': row.cnpj}
        company = self.company_repo.get_or_create(company_data)

        if not buy_order:
            raise Exception('BuyOrder does not exist')

        ecs_buy_order_data: EcsBuyOrderDataType = {
            'buy_order': buy_order,
            'ecs_order_id': row.ecs_order_id,
            'ecs_order_number': row.ecs_order_number,
            'company': company,
            'coupon': row.coupon,
            'deadline_days': row.deadline_days,
            'ecs_carrier': row.carrier,
            'ecs_delivery_date': row.ecs_delivery_date,
            'payment_date': row.payment_date,
            'recipient_name': row.recipient_name,
            'recipient_city': row.recipient_city,
            'recipient_state': row.recipient_state,
            'recipient_zip_code': row.recipient_zip_code,
        }

        self.ecs_buy_order_repo.upsert(ecs_buy_order_data)
