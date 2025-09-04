from typing import Optional

import pandas as pd

from core.ingestion.base_extractor import BaseExtractor
from core.typings.file_types import CsvSource

from .schemas import COLUMN_ALIASES


class BuyOrderCsvExtractor(BaseExtractor):
    def __init__(self, csv_file: CsvSource) -> None:
        self.csv_file: CsvSource = csv_file
        self.df: Optional[pd.DataFrame] = None

    def extract(self) -> pd.DataFrame:
        df = self._load_csv()
        df = df.rename(columns=COLUMN_ALIASES)
        df = self._remove_totals_row(df)
        self.df = df
        return df

    def _load_csv(self) -> pd.DataFrame:
        try:
            df: pd.DataFrame = pd.read_csv(
                self.csv_file,
                sep=',',
                dtype=str,
                encoding='utf-8',
            )
            return df
        except FileNotFoundError:
            raise ValueError(f'File not found in the path: {self.csv_file}')
        except Exception as e:
            raise ValueError(f'Error on read csv file: {e}')

    def _remove_totals_row(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Remove last row if "order_number" column == "totais"
        """
        verify_column = 'order_number'
        value = 'totais'
        if not df.empty and verify_column in df.columns:
            last_row = df.iloc[-1]
            last_row_value = str(last_row[verify_column]).strip().lower()
            if last_row_value == value.lower():
                df = df.iloc[:-1]
        return df
