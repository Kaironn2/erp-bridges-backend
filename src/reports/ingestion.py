from typing import TypedDict

from mgt.ingestion.buy_order_csv.pipeline import BuyOrderCsvPipeline
from mgt.ingestion.customer_csv.pipeline import CustomerCsvPipeline


class IngestionMappingType(TypedDict):
    mgt_buy_orders_csv: type[BuyOrderCsvPipeline]
    mgt_customers_csv: type[CustomerCsvPipeline]


REPORT_MAP: IngestionMappingType = {
    'mgt_buy_orders_csv': BuyOrderCsvPipeline,
    'mgt_customers_csv': CustomerCsvPipeline,
}
