from abc import ABC, abstractmethod
from typing import Any, final

from pandas import DataFrame


class BasePipeline(ABC):
    @final
    def run(self, source: Any):
        df = self._extract(source)
        df = self._transform(df)
        self._load(df)

    @abstractmethod
    def _extract(self, source: Any) -> DataFrame: ...

    @abstractmethod
    def _transform(self, df: DataFrame) -> DataFrame: ...

    @abstractmethod
    def _load(self, df: DataFrame) -> None: ...
