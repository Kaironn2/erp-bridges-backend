from typing import TypedDict

from mgt.ingestion.buy_order_csv.pipeline import BuyOrderCsvPipeline
from mgt.ingestion.customer_csv.pipeline import CustomerCsvPipeline


class IngestionMappingType(TypedDict):
    buy_order_csv: type[BuyOrderCsvPipeline]
    customer_csv: type[CustomerCsvPipeline]


REPORT_MAPPING: IngestionMappingType = {
    'buy_order_csv': BuyOrderCsvPipeline,
    'customer_csv': CustomerCsvPipeline,
}
