import pandas as pd

from core.ingestion.base_transformer import BaseTransformer
from utils.dataframe_utils import DataFrameUtils as dfu


class BuyOrderCsvTransformer(BaseTransformer):
    def __init__(self, df: pd.DataFrame):
        self.df = df

    def transform(self) -> pd.DataFrame:
        self.df = self._lower_case_columns(self.df)
        self.df = self._clean_currency_columns(self.df)
        self.df = self._convert_date_columns(self.df)
        self.df = self._keep_only_digits_columns(self.df)
        self.df = dfu.replace_nulls_with_none(self.df)
        return self.df

    def _lower_case_columns(self, df: pd.DataFrame) -> pd.DataFrame:
        columns = ['first_name', 'last_name', 'email', 'customer_group', 'status']
        return dfu.lower_case_values(df, columns)

    def _clean_currency_columns(self, df: pd.DataFrame) -> pd.DataFrame:
        columns = ['shipping_amount', 'discount_amount', 'total_amount']
        return dfu.clean_currency_columns(df, columns, symbol='R$')

    def _convert_date_columns(self, df: pd.DataFrame) -> pd.DataFrame:
        columns = ['order_date']
        date_format = '%d/%m/%Y %H:%M:%S'
        df = dfu.convert_to_datetime(df, columns, date_format)
        return dfu.convert_dataframe_datetimes_to_aware(df, columns)

    def _keep_only_digits_columns(self, df: pd.DataFrame) -> pd.DataFrame:
        columns = ['cpf', 'phone']
        return dfu.keep_only_digits(df, columns)

    def _replace_columns_values(self, df: pd.DataFrame) -> pd.DataFrame:
        mapping = {
            'payment_type': {
                'pix': 'pix',
                'cartão': 'cartão de crédito',
                'boleto': 'boleto bancário',
                'necessário': 'saldo',
            }
        }
        return dfu.replace_values(df, mapping, contains=True)
