from typing import TypedDict

from reports.ingestion.buy_order_csv.pipeline import BuyOrderCsvPipeline
from reports.ingestion.customer_csv.pipeline import CustomerCsvPipeline
from reports.ingestion.ecs_buy_order_csv.pipeline import EcsBuyOrderCsvPipeline


class IngestionMappingType(TypedDict):
    buy_orders_csv: type[BuyOrderCsvPipeline]
    customers_csv: type[CustomerCsvPipeline]
    ecs_buy_orders_csv: type[EcsBuyOrderCsvPipeline]


REPORT_MAP: IngestionMappingType = {
    'buy_orders_csv': BuyOrderCsvPipeline,
    'customers_csv': CustomerCsvPipeline,
    'ecs_buy_orders_csv': EcsBuyOrderCsvPipeline,
}
