from abc import ABC, abstractmethod
from typing import Dict, Generic, List, Type, TypeVar

import pandas as pd
from pydantic import BaseModel, ValidationError

from reports.utils.dataframe_utils import DataFrameUtils as dfu

SchemaType = TypeVar('SchemaType', bound=BaseModel)


class BaseReportAdapter(ABC, Generic[SchemaType]):
    """An abstract, generic base class for creating report adapters.

    This class provides a standardized pipeline for reading a data source,
    cleaning it based on declarative rules, and validating it against a
    specific Pydantic schema.

    It is designed to be subclassed. The cleaning behavior is configured
    by overriding the attributes in the inner `Meta` class. The data loading
    logic must be provided by implementing the `load_raw_data_to_df` method.

    Example of a concrete implementation:
        class MyCsvAdapter(BaseReportAdapter[MySchema]):
            class Meta:
                currency_columns = ['Price']
                date_format = '%Y-%m-%d'

            def load_raw_data_to_df(self, file_path):
                return pd.read_csv(file_path)
    """
    class Meta:
        """
        Inner class for declarative configuration of the cleaning pipeline.
        Subclasses should override these attributes as needed.
        """
        currency_columns: List[str] = []
        datetime_columns: List[str] = []
        date_format: str = ''
        keep_only_digits_columns: List[str] = []
        lower_case_columns: List[str] = []
        columns_mapping: Dict[str, Dict] = {}
        mapping_contains: bool = True
        split_columns: Dict[str, Dict] = {}
        split_columns_sep = ' '
        rename_columns: Dict[str, str] = {}

    def __init__(self, file_path_or_buffer):
        """Initializes the adapter by loading data and setting up configuration."""
        self.df = self.load_raw_data_to_df(file_path_or_buffer)
        self._setup_config()

    @abstractmethod
    def load_raw_data_to_df(self, file_path_or_buffer) -> pd.DataFrame:
        """Abstract method to be implemented by subclasses.

        Its responsibility is to read a data source (e.g., a CSV, Excel file,
        or database query) and return it as a pandas DataFrame.

        Args:
            file_path_or_buffer: The source of the data, e.g., a file path
                or an in-memory buffer.

        Returns:
            pd.DataFrame: The loaded data as a pandas DataFrame.
        """
        raise NotImplementedError

    def _get_schema_class(self) -> Type[SchemaType]:
        """Introspects the subclass to find the concrete Pydantic schema type."""
        try:
            return self.__class__.__orig_bases__[0].__args__[0]
        except (AttributeError, IndexError):
            raise TypeError(
                f'The class {self.__class__.__name__} must inherit from BaseReportAdapter '
                'with a valid Pydantic schema type defined in Meta.schema_class '
                '(e.g., MyAdapter(BaseReportAdapter) with Meta.schema_class = MySchema).'
            )

    def _setup_config(self) -> None:
        """
        Reads configurations from the Meta class and sets them as instance
        attributes, providing safe defaults for any missing values.
        """
        self.currency_columns = getattr(self.Meta, 'currency_columns', [])
        self.datetime_columns = getattr(self.Meta, 'datetime_columns', [])
        self.date_format = getattr(self.Meta, 'date_format', '')
        self.keep_only_digits_columns = getattr(self.Meta, 'keep_only_digits_columns', [])
        self.lower_case_columns = getattr(self.Meta, 'lower_case_columns', [])
        self.replace_mapping = getattr(self.Meta, 'columns_mapping', {})
        self.replace_contains = getattr(self.Meta, 'replace_contains', False)
        self.split_columns = getattr(self.Meta, 'split_columns', {})
        self.split_separator = getattr(self.Meta, 'split_columns_sep', ' ')
        self.rename_columns = getattr(self.Meta, 'rename_columns', {})

    def _clean_dataframe(self) -> pd.DataFrame:
        """Applies the full cleaning pipeline using pre-configured instance attributes."""
        self.df = dfu.split_column(self.df, self.split_columns, self.split_separator)
        self.df = dfu.clean_currency_columns(self.df, self.currency_columns)
        self.df = dfu.convert_to_datetime(self.df, self.datetime_columns, self.date_format)
        self.df = dfu.keep_only_digits(self.df, self.keep_only_digits_columns)
        self.df = dfu.lower_case_values(self.df, self.lower_case_columns)
        self.df = dfu.replace_values(self.df, self.replace_mapping, self.replace_contains)
        self.df = dfu.empty_strings_to_none(self.df)
        self.df = self.df.rename(self.rename_columns)

        return self.df

    def process(self) -> List[SchemaType]:
        """Orchestrates the cleaning, structuring, and validation of the data.

        This is the main public method that executes the full ETL pipeline for the
        adapter, returning a list of validated Pydantic objects.

        Returns:
            List[SchemaType]: A list of validated Pydantic model instances.

        Raises:
            ValueError: If Pydantic validation fails for any row.
        """
        if self.df.empty:
            return []

        schema_class = self._get_schema_class()
        cleaned_df: pd.DataFrame = self._clean_dataframe()
        records = cleaned_df.to_dict(orient='records')

        try:
            return [schema_class.model_validate(rec) for rec in records]
        except ValidationError as e:
            raise ValueError(f'Pydantic validation error {e}')
