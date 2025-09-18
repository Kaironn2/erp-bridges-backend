from typing import TypedDict

from reports.ingestion.buy_order_csv.pipeline import BuyOrderCsvPipeline
from reports.ingestion.customer_csv.pipeline import CustomerCsvPipeline


class IngestionMappingType(TypedDict):
    buy_orders_csv: type[BuyOrderCsvPipeline]
    customers_csv: type[CustomerCsvPipeline]


REPORT_MAP: IngestionMappingType = {
    'buy_orders_csv': BuyOrderCsvPipeline,
    'customers_csv': CustomerCsvPipeline,
}
