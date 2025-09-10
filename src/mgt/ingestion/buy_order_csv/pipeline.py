import pandas as pd

from core.ingestion.base_pipeline import BasePipeline
from core.typings.file_types import CsvSource
from mgt.ingestion.buy_order_csv.extractor import BuyOrderCsvExtractor
from mgt.ingestion.buy_order_csv.loader import BuyOrderCsvLoader
from mgt.ingestion.buy_order_csv.transformer import BuyOrderCsvTransformer


class BuyOrderCsvPipeline(BasePipeline):
    def _extract(self, source: CsvSource) -> pd.DataFrame:
        extractor = BuyOrderCsvExtractor(source)
        return extractor.extract()

    def _transform(self, df: pd.DataFrame) -> pd.DataFrame:
        transformer = BuyOrderCsvTransformer(df)
        return transformer.transform()

    def _load(self, df: pd.DataFrame) -> None:
        loader = BuyOrderCsvLoader(df)
        loader.load()
