import numpy as np
import pandas as pd

from core.ingestion.base_transformer import BaseTransformer
from utils.dataframe_utils import DataFrameUtils as dfu
from utils.load_shipping_methods import load_shipping_methods


class EcsBuyOrderCsvTransformer(BaseTransformer):
    def __init__(self, df: pd.DataFrame):
        self.df = df

    def transform(self) -> pd.DataFrame:
        self.df = self._lower_case_columns(self.df)
        self.df = self._convert_date_columns(self.df)
        self.df = self._keep_only_digits_columns(self.df)
        self.df = self._extract_cnpj_from_details(self.df)
        self.df = self._extract_deadline_days(self.df)
        self.df = self._extract_coupon(self.df)
        self.df = self._replace_columns_values(self.df)
        self.df = self._replace_carrier_with_carrier_type(self.df)
        self.df = dfu.replace_nulls_with_none(self.df)
        return self.df

    def _lower_case_columns(self, df: pd.DataFrame) -> pd.DataFrame:
        columns = [
            'recipient_name',
            'recipient_city',
            'recipient_state',
            'details',
            'carrier',
            'carrier_type',
            'payment_type',
        ]
        return dfu.lower_case_values(df, columns)

    def _convert_date_columns(self, df: pd.DataFrame) -> pd.DataFrame:
        df['ecs_delivery_date'] = df['ecs_delivery_date'].replace(
            to_replace=r'^0{4}-0{2}-0{2}\s+0{2}:0{2}:0{2}', value=None, regex=True
        )
        columns_1 = ['ecs_delivery_date']

        date_format_1 = '%d/%m/%Y %H:%M:%S'
        df = dfu.convert_to_datetime(df, columns_1, date_format_1)

        columns_2 = ['payment_date']
        date_format_2 = '%d/%m/%Y'
        df = dfu.convert_to_datetime(df, columns_2, date_format_2)

        columns = columns_1 + columns_2
        return dfu.convert_dataframe_datetimes_to_aware(df, columns)

    def _keep_only_digits_columns(self, df: pd.DataFrame) -> pd.DataFrame:
        columns = ['recipient_zip_code']
        return dfu.keep_only_digits(df, columns)

    def _extract_cnpj_from_details(self, df: pd.DataFrame) -> pd.DataFrame:
        if 'details' in df.columns:
            df['cnpj'] = np.where(
                df['details'].str.contains('free', case=False, na=False),
                np.nan,
                df['details'].str.extract(r'cnpj_(\d{14})')[0],
            )
        return df

    def _extract_deadline_days(self, df: pd.DataFrame) -> pd.DataFrame:
        if 'details' in df.columns:
            df['deadline_days'] = (
                df['details'].str.extract(r'média\s+(\d+)')[0].fillna(0).astype(int)
            )
        return df

    def _extract_coupon(self, df: pd.DataFrame) -> pd.DataFrame:
        PAYMENTS = ['pagarme5_cc', 'pagarme5_pix', 'pagarme5_boleto', 'free']

        def get_coupon(details: str) -> str | None:
            if not isinstance(details, str) or not details.strip():
                return None
            parts = details.split()
            last = parts[-1]
            return None if last in PAYMENTS else last

        df['coupon'] = df['details'].apply(get_coupon)
        return df

    def _replace_columns_values(self, df: pd.DataFrame) -> pd.DataFrame:
        mapping_1 = {'carrier': load_shipping_methods()}
        df = dfu.replace_values(df, mapping_1, contains=True)

        mapping_2 = {
            'payment_type': {
                'pix': 'pix',
                'cartão': 'cartão de crédito',
                'boleto': 'boleto bancário',
                'loja': 'saldo',
            }
        }

        return dfu.replace_values(df, mapping_2, contains=True)

    def _replace_carrier_with_carrier_type(self, df: pd.DataFrame) -> pd.DataFrame:
        if 'carrier' in df.columns and 'carrier_type' in df.columns:
            mask = df['carrier'].str.lower() == 'correios'
            df.loc[mask, 'carrier'] = df.loc[mask, 'carrier_type']
        return df
