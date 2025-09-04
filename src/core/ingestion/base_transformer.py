from abc import ABC, abstractmethod

import pandas as pd


class BaseTransformer(ABC):
    @abstractmethod
    def transform(self) -> pd.DataFrame:
        raise NotImplementedError('transform method must be implemented')
