import pandas as pd

from core.ingestion.base_transformer import BaseTransformer

from utils.dataframe_utils import DataFrameUtils as dfu


class InvoiceXmlTransformer(BaseTransformer):
    def __init__(self, df: pd.DataFrame):
        self.df = df

    def transform(self) -> pd.DataFrame:
        self.df = self._lower_case_columns(self.df)
        self.df = self._keep_only_digits_columns(self.df)
        self.df = dfu.replace_nulls_with_none(self.df)
        return self.df

    def _lower_case_columns(self, df: pd.DataFrame):
        columns = [
            'operation_nature',
            'name',
            'street',
            'complement',
            'neighborhood',
            'city',
            'state',
            'country',
        ]
        return dfu.lower_case_values(df, columns)

    def _keep_only_digits_columns(self, df: pd.DataFrame) -> pd.DataFrame:
        columns = ['cpf', 'zip_code', 'phone']
        return dfu.keep_only_digits(df, columns)
