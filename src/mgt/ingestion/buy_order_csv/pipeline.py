from typing import Any

import pandas as pd

from core.ingestion.base_pipeline import BasePipeline
from mgt.ingestion.buy_order_csv.extractor import BuyOrderCsvExtractor
from mgt.ingestion.buy_order_csv.loader import BuyOrderCsvLoader
from mgt.ingestion.buy_order_csv.transformer import BuyOrderCsvTransformer


class BuyOrderCsvPipeline(BasePipeline):
    def extract(self, source: Any) -> pd.DataFrame:
        extractor = BuyOrderCsvExtractor(source)
        return extractor.extract()

    def transform(self, df: pd.DataFrame) -> pd.DataFrame:
        transformer = BuyOrderCsvTransformer(df)
        return transformer.transform()

    def load(self, df: pd.DataFrame) -> None:
        loader = BuyOrderCsvLoader(df)
        loader.load()
