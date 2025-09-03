from abc import ABC, abstractmethod


class BaseLoader(ABC):
    @abstractmethod
    def load(self) -> None:
        raise NotImplementedError('load method must be implemented')
