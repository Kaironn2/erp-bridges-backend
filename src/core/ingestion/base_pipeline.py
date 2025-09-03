from abc import ABC, abstractmethod
from typing import Any, final

from pandas import DataFrame


class BasePipeline(ABC):
    @final
    def run(self, source: Any):
        df = self.extract(source)
        df = self.transform(df)
        self.load(df)

    @abstractmethod
    def extract(self, source: Any) -> DataFrame: ...

    @abstractmethod
    def transform(self, df: DataFrame) -> DataFrame: ...

    @abstractmethod
    def load(self, df: DataFrame) -> None: ...
