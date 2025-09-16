import pandas as pd

from core.ingestion.base_pipeline import BasePipeline
from core.typings.file_types import CsvSource
from reports.ingestion.customer_csv.extractor import CustomerCsvExtractor
from reports.ingestion.customer_csv.loader import CustomerCsvLoader
from reports.ingestion.customer_csv.transformer import CustomerCsvTransformer


class CustomerCsvPipeline(BasePipeline):
    def _extract(self, source: CsvSource) -> pd.DataFrame:
        extractor = CustomerCsvExtractor(source)
        return extractor.extract()

    def _transform(self, df: pd.DataFrame) -> pd.DataFrame:
        transformer = CustomerCsvTransformer(df)
        return transformer.transform()

    def _load(self, df: pd.DataFrame) -> None:
        loader = CustomerCsvLoader(df)
        loader.load()
