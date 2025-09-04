from abc import ABC, abstractmethod

import pandas as pd


class BaseExtractor(ABC):
    @abstractmethod
    def extract(self) -> pd.DataFrame:
        raise NotImplementedError('extract method must be implemented')
