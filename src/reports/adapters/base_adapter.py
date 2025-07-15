from abc import ABC, abstractmethod
from typing import Dict, Generic, List, Type, TypeVar

import pandas as pd
from pydantic import BaseModel, ValidationError

from reports.utils.dataframe_utils import DataFrameUtils as dfu

SchemaType = TypeVar('SchemaType', bound=BaseModel)


class BaseReportAdapter(ABC, Generic[SchemaType]):
    class Meta:
        currency_columns: List[str] = []
        datetime_columns: List[str] = []
        date_format: str = ''
        keep_only_digits_columns: List[str] = []
        lower_case_columns: List[str] = []
        columns_mapping: Dict[str, Dict] = {}
        mapping_contains: bool = True
        split_columns: Dict[str, Dict] = {}
        split_columns_sep = ' '

    def __init__(self, file_path_or_buffer):
        self.df = self.load_raw_data_to_df(file_path_or_buffer)
        self._setup_meta()

    @abstractmethod
    def load_raw_data_to_df(self, file_path_or_buffer) -> pd.DataFrame:
        raise NotImplementedError

    def _get_schema_class(self) -> Type[SchemaType]:
        try:
            return self.__class__.__orig_bases__[0].__args__[0]
        except (AttributeError, IndexError):
            raise TypeError(
                f'The class {self.__class__.__name__} must inherit from BaseReportAdapter '
                'with a valid Pydantic schema type defined in Meta.schema_class '
                '(e.g., MyAdapter(BaseReportAdapter) with Meta.schema_class = MySchema).'
            )

    def _setup_meta(self) -> None:
        self.Meta.currency_columns = getattr(self.Meta, 'currency_columns', [])
        self.Meta.datetime_columns = getattr(self.Meta, 'datetime_columns', [])
        self.Meta.date_format = getattr(self.Meta, 'date_format', '')
        self.Meta.keep_only_digits_columns = getattr(self.Meta, 'keep_only_digits_columns', [])
        self.Meta.lower_case_columns = getattr(self.Meta, 'lower_case_columns', [])
        self.Meta.columns_mapping = getattr(self.Meta, 'columns_mapping', {})
        self.Meta.mapping_contains = getattr(self.Meta, 'mapping_contains', False)
        self.Meta.split_columns = getattr(self.Meta, 'split_columns', {})
        self.Meta.split_columns_sep = getattr(self.Meta, 'split_columns_sep', False)

    def _clean_dataframe(self) -> pd.DataFrame:
        self.df = dfu.split_column(self.df, self.Meta.split_columns, self.Meta.split_columns_sep)
        self.df = dfu.clean_currency_columns(self.df, self.Meta.currency_columns)
        self.df = dfu.convert_to_datetime(
            self.df, self.Meta.datetime_columns, self.Meta.date_format
        )
        self.df = dfu.keep_only_digits(self.df, self.Meta.keep_only_digits_columns)
        self.df = dfu.lower_case_values(self.df, self.Meta.lower_case_columns)
        self.df = dfu.replace_values(
            self.df, self.Meta.columns_mapping, self.Meta.mapping_contains
        )
        self.df = dfu.empty_strings_to_none(self.df)
        return self.df

    def process(self) -> List[SchemaType]:
        if self.df.empty:
            return []

        schema_class = self._get_schema_class()
        cleaned_df: pd.DataFrame = self._clean_dataframe()
        records = cleaned_df.to_dict(orient='records')

        try:
            if hasattr(schema_class, 'from_flat_dict') and callable(
                getattr(schema_class, 'from_flat_dict')
            ):
                return [schema_class.from_flat_dict(rec) for rec in records]
            else:
                return [schema_class.model_validate(rec) for rec in records]
        except ValidationError as e:
            raise ValueError(f'Pydantic validation error {e}')
