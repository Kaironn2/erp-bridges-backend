import pandas as pd

from core.ingestion.base_transformer import BaseTransformer
from utils.dataframe_utils import DataFrameUtils as dfu
from utils.load_shipping_methods import load_shipping_methods


class BuyOrderCsvTransformer(BaseTransformer):
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
        ]
        return dfu.lower_case_values(df, columns)

    def _convert_date_columns(self, df: pd.DataFrame) -> pd.DataFrame:
        df['ecs_delivery_date'] = df['ecs_delivery_date'].replace(
            to_replace=r'^0{4}-0{2}-0{2}\s+0{2}:0{2}:0{2}$', value=None, regex=True
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
            df['cnpj'] = df['details'].str.extract(r'cnpj_(\d{14})')
        return df

    def _extract_deadline_days(self, df: pd.DataFrame) -> pd.DataFrame:
        if 'details' in df.columns:
            df['deadline_days'] = df['details'].str.extract(r'média\s+(\d+)')
        return df

    def _extract_coupon(self, df: pd.DataFrame) -> pd.DataFrame:
        if 'details' in df.columns:
            pattern = r'Meio de pagamento:[^\S\r\n]*\S+\s+(\S+)'
            df['coupon'] = df['details'].str.extract(pattern, expand=False)

            df['coupon'] = df['coupon'].str.strip().str.rstrip('.,;:')
            df['coupon'] = df['coupon'].where(df['coupon'].notna(), None)
        return df

    def _replace_columns_values(self, df: pd.DataFrame) -> pd.DataFrame:
        mapping = {'carrier': load_shipping_methods()}
        return dfu.replace_values(df, mapping, contains=True)

    def _replace_carrier_with_carrier_type(self, df: pd.DataFrame) -> pd.DataFrame:
        if 'carrier' in df.columns and 'carrier_type' in df.columns:
            mask = df['carrier'].str.lower() == 'correios'
            df.loc[mask, 'carrier'] = df.loc[mask, 'carrier_type']
        return df
