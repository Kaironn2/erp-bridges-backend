import pandas as pd

from core.ingestion.base_pipeline import BasePipeline
from reports.ingestion.invoice_xml.extractor import InvoiceXmlExtractor
from reports.ingestion.invoice_xml.transformer import InvoiceXmlTransformer
from reports.ingestion.invoice_xml.loader import InvoiceXmlLoader


class BuyOrderCsvPipeline(BasePipeline):
    def _extract(self, source) -> pd.DataFrame:
        extractor = InvoiceXmlExtractor(source)
        return extractor.extract()

    def _transform(self, df: pd.DataFrame) -> pd.DataFrame:
        transformer = InvoiceXmlTransformer(df)
        return transformer.transform()

    def _load(self, df: pd.DataFrame) -> None:
        loader = InvoiceXmlLoader(df)
        loader.load()
