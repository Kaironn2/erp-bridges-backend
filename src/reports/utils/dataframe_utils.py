from typing import Any, Dict, List, Tuple

import pandas as pd

from reports.utils.datetime_utils import local_to_aware
from reports.utils.monetary import to_decimal


class DataFrameUtils:
    """Utily class with static methods for operations with dataframes"""

    @staticmethod
    def clean_currency_columns(
        df: pd.DataFrame, columns: List[str], symbol: str = 'R$'
    ) -> pd.DataFrame:
        """Converts string-formatted monetary columns to `Decimal` objects.

        This method is designed to clean currency strings in a typical
        Brazilian format (e.g., "R$ 1.234,56"). It strips the currency
        symbol, removes thousand separators, and replaces the decimal comma
        with a period before converting the value to a high-precision Decimal.

        Args:
            df (pd.DataFrame): The input DataFrame to process.
            columns (List[str]): A list of column names to convert.
            symbol (str, optional): The currency symbol to strip.
            Defaults to 'R$'.

        Returns:
            pd.DataFrame: The DataFrame with specified columns converted to
            the `Decimal` data type.
        """
        for col in columns:
            if col not in df.columns:
                continue

            cleaned_series = (
                df[col]
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
        """Replaces values in specified columns based on per-column mappings.

        This method supports two replacement strategies based on the 'contains'
        flag:
        - Exact match: Replaces a cell's value only if it exactly matches a
          key in the mapping dictionary.
        - Substring match: Replaces a cell's entire value if it contains a
          key from the mapping dictionary as a substring.

        Args:
            df (pd.DataFrame): The input DataFrame to process.
            columns_mapping (Dict[str, Dict[str, Any]]): A dictionary where keys
                are column names and values are the replacement mappings for
                that column (e.g., {'col_name': {'old_val': 'new_val'}}).
            contains (bool): The replacement strategy. If False, uses exact
                matching. If True, uses substring matching.

        Returns:
            pd.DataFrame: The DataFrame with values replaced in the specified
            columns.
        """
        for col, mapping in columns_mapping.items():
            if col not in df.columns:
                continue

            if contains:
                for find_val, replace_val in mapping.items():
                    mask = df[col].str.contains(find_val, na=False, regex=False)
                    df.loc[mask, col] = replace_val
            else:
                df[col] = df[col].replace(mapping)

        return df

    @staticmethod
    def convert_to_datetime(
        df: pd.DataFrame, columns: List[str], date_format: str
    ) -> pd.DataFrame:
        """Converts string columns to datetime objects using a specified format.

        This method leverages pandas.to_datetime with error coercion, which
        will turn any unparseable date strings into NaT (Not a Time) instead
        of raising an error.

        Args:
            df (pd.DataFrame): The input DataFrame to process.
            columns (List[str]): A list of column names to convert.
            date_format (str): The expected date format string, following
            strftime conventions (e.g., '%d/%m/%Y %H:%M:%S').

        Returns:
            pd.DataFrame: The DataFrame with the specified columns converted
            to the datetime data type.
        """
        for col in columns:
            if col not in df.columns:
                continue

            df[col] = pd.to_datetime(df[col], format=date_format, errors='coerce')

        return df

    @staticmethod
    def keep_only_digits(df: pd.DataFrame, columns: List[str]) -> pd.DataFrame:
        """Removes all non-digit characters from specified columns.

        This method is ideal for cleaning formatted strings like phone numbers,
        postal codes (CEP), or document IDs by using a regular expression
        to strip any character that is not a numeric digit (0-9).

        Args:
            df (pd.DataFrame): The input DataFrame to process.
            columns (List[str]): A list of column names to clean.

        Returns:
            pd.DataFrame: The DataFrame with the specified columns containing
            only digits.
        """
        for col in columns:
            if col not in df.columns:
                continue

            df[col] = df[col].str.replace(r'\D', '', regex=True)

        return df

    @staticmethod
    def lower_case_values(df: pd.DataFrame, columns: List[str]) -> pd.DataFrame:
        """Converts string values in specified DataFrame columns to lowercase.

        Args:
            df (pd.DataFrame): The DataFrame to process.
            columns (List[str]): The names of the columns to convert to lowercase.

        Returns:
            pd.DataFrame: The DataFrame with the specified columns lowercased.
        """
        for col in columns:
            if col not in df.columns:
                continue

            df[col] = df[col].str.lower()

        return df

    @staticmethod
    def empty_strings_to_none(df: pd.DataFrame) -> pd.DataFrame:
        """Replaces empty or whitespace-only strings with np.nan across the DataFrame.

        This method uses a regular expression to find all cells containing
        either an empty string or only whitespace characters and replaces them
        with a standard null value (np.nan).

        Args:
            df (pd.DataFrame): The input DataFrame to be processed.

        Returns:
            pd.DataFrame: A new DataFrame with empty strings replaced by np.nan.
        """
        return df.replace(r'^\s*$', None, regex=True)

    @staticmethod
    def split_column(
        df: pd.DataFrame,
        columns_mapping: Dict[str, Tuple[str, str]],
        sep=' ',
    ) -> pd.DataFrame:
        for col, mapping in columns_mapping.items():
            if col not in df.columns:
                continue

            split_df = df[col].str.split(sep, n=1, expand=True)
            df[mapping[0]] = split_df[0]
            df[mapping[1]] = split_df[1]

        return df

    @staticmethod
    def convert_dataframe_datetimes_to_aware(
        df: pd.DataFrame, datetime_columns: list
    ) -> pd.DataFrame:
        """
        Converts data columns in DataFrame to time zone awareness (America/Sao_Paulo).
        """
        for col in datetime_columns:
            if col in df.columns:
                df[col] = pd.to_datetime(df[col], errors='coerce')
                df[col] = df[col].apply(local_to_aware)

        return df
