import pandas as pd

from core.ingestion.base_transformer import BaseTransformer
from utils.dataframe_utils import DataFrameUtils as dfu


class CustomerCsvTransformer(BaseTransformer):
    def __init__(self, df: pd.DataFrame):
        self.df = df

    def transform(self) -> pd.DataFrame:
        self.df = self._split_columns(self.df)
        self.df = self._lower_case_columns(self.df)
        self.df = self._convert_date_columns(self.df)
        self.df = self._keep_only_digits_columns(self.df)
        self.df = dfu.replace_nulls_with_none(self.df)
        return self.df

    def _split_columns(self, df: pd.DataFrame) -> pd.DataFrame:
        mapping = {'name': ('first_name', 'last_name')}
        return dfu.split_column(df, mapping)

    def _lower_case_columns(self, df: pd.DataFrame) -> pd.DataFrame:
        columns = ['first_name', 'last_name', 'email', 'customer_group', 'state', 'country']
        return dfu.lower_case_values(df, columns)

    def _convert_date_columns(self, df: pd.DataFrame) -> pd.DataFrame:
        columns = ['customer_since']
        date_format = '%d/%m/%Y %H:%M:%S'
        df = dfu.convert_to_datetime(df, columns, date_format)
        return dfu.convert_dataframe_datetimes_to_aware(df, columns)

    def _keep_only_digits_columns(self, df: pd.DataFrame) -> pd.DataFrame:
        columns = ['phone', 'postal_code']
        return dfu.keep_only_digits(df, columns)
