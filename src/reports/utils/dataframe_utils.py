from typing import Any, Dict, List

import pandas as pd

from reports.utils.monetary import to_decimal


class DataFrameUtils:
    """Utily class with static methods for operations with dataframes"""
    @staticmethod
    def clean_currency_columns(
        df: pd.DataFrame, columns: List[str], symbol: str = 'R$'
    ) -> pd.DataFrame:
        """Convert columns with monetary values string to python Decimal object

        Args:
            df (pd.DataFrame): dataframe with str monetary values
            columns (List[str]): columns to clean
            symbol (str, optional): Monetary symbol to replace. Defaults to 'R$'.

        Returns:
            pd.DataFrame: returns the dataframe with the columns converted to Decimal
        """
        for col in columns:
            if col not in df.columns:
                continue

            cleaned_series = (
                df[col].astype(str)
                .str.replace(symbol, '', regex=False)
                .str.strip()
                .str.replace('.', '', regex=False)
                .str.replace(',', '.', regex=False)
            )
            df[col] = cleaned_series.apply(to_decimal)

        return df

    @staticmethod
    def replace_values(
        df: pd.DataFrame, columns_mapping: Dict[str, Dict[str, Any]], contains: bool
    ) -> pd.DataFrame:
        """Replace values in series using a mapping with source and target values

        Args:
            df (pd.DataFrame): dataframe with values to replace
            columns mapping (Dict[str, Dict[str, Any]]): columns to apply replacements and ur mappings
            contains (bool): false to exact replacement, true for contains

        Returns:
            pd.DataFrame: dataframe with values replaceds
        """  # noqa: E501
        for col, mapping in columns_mapping.items():
            if col not in df.columns:
                continue

            if contains:
                for find_val, replace_val in mapping.items():
                    mask = df[col].astype(str).str.contains(
                        find_val, na=False, regex=False
                    )
                    df.loc[mask, col] = replace_val
            else:
                df[col] = df[col].replace(mapping)

        return df

    @staticmethod
    def convert_to_datetime(
        df: pd.DataFrame, columns: List[str], date_format: str
    ) -> pd.DataFrame:
        """convert str in the date_format arg to datetime

        Args:
            df (pd.DataFrame): dataframe with values to convert
            columns (List[str]): columns to apply conversion
            date_format (str): str values date format

        Returns:
            pd.DataFrame: dataframe with the values converted in datetime
        """
        for col in columns:
            if col not in df.columns:
                continue

            df[col] = pd.to_datetime(df[col], format=date_format, errors='coerce')

        return df

    @staticmethod
    def keep_only_digits(df: pd.DataFrame, columns: List[str]) -> pd.DataFrame:
        """removes characteres, keeping only numeric digits. Used to phone, CEP etc

        Args:
            df (pd.DataFrame): dataframe with values to clean
            columns (List[str]): columns to remove characteres

        Returns:
            pd.DataFrame: dataframe with colums containing only numeric digits
        """
        for col in columns:
            if col not in df.columns:
                continue

            df[col] = df[col].astype(str).str.replace(r'\D', '', regex=True)

        return df

    @staticmethod
    def lower_case_values(df: pd.DataFrame, columns: List[str]) -> pd.DataFrame:
        """lowercase all values in the columns

        Args:
            df (pd.DataFrame): dataframe with values to lowercase
            columns (List[str]): columns to apply lowercase in the values

        Returns:
            pd.DataFrame: dataframe with lowercase columns values
        """
        for col in columns:
            if col not in df.columns:
                continue

            df[col] = df[col].astype(str).str.lower()

        return df
