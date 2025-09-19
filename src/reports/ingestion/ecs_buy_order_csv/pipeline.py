import pandas as pd

from core.ingestion.base_pipeline import BasePipeline
from core.typings.file_types import CsvSource
from reports.ingestion.ecs_buy_order_csv.extractor import EcsBuyOrderCsvExtractor
from reports.ingestion.ecs_buy_order_csv.loader import EcsBuyOrderCsvLoader
from reports.ingestion.ecs_buy_order_csv.transformer import EcsBuyOrderCsvTransformer


class EcsBuyOrderCsvPipeline(BasePipeline):
    def _extract(self, source: CsvSource) -> pd.DataFrame:
        extractor = EcsBuyOrderCsvExtractor(source)
        return extractor.extract()

    def _transform(self, df: pd.DataFrame) -> pd.DataFrame:
        transformer = EcsBuyOrderCsvTransformer(df)
        return transformer.transform()

    def _load(self, df: pd.DataFrame) -> None:
        loader = EcsBuyOrderCsvLoader(df)
        loader.load()
