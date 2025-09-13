import pandas as pd
from django.db import transaction

from core.ingestion.base_loader import BaseLoader


class EcsOrderCsvLoader(BaseLoader):
    def __init__(self, df: pd.DataFrame) -> None:
        self.df = df

    def load(self) -> None:
        with transaction.atomic():
            ...
