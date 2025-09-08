import pandas as pd

from core.ingestion.base_extractor import BaseExtractor
from core.typings.file_types import CsvSource

from .schemas import COLUMN_ALIASES


class CustomerCsvExtractor(BaseExtractor):
    def __init__(self, csv_file: CsvSource) -> None:
        self.csv_file: CsvSource = csv_file

    def extract(self) -> pd.DataFrame:
        df = self._load_csv()
        df = df.rename(columns=COLUMN_ALIASES)
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
