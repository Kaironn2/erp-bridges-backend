from abc import ABC, abstractmethod
from typing import Any, Dict


class BaseReportStrategy(ABC):
    """
    Abstract base class for all report processing strategies.

    It defines a common interface that all concrete strategies must follow,
    ensuring they have a `process` method.
    """

    def __init__(self, file_path_or_buffer):
        """
        Initializes the strategy with the source file.

        Args:
            file_path_or_buffer: The path to the source file or an
                in-memory buffer.
        """
        if not file_path_or_buffer:
            raise ValueError('A file path or buffer must be provided.')
        self.file = file_path_or_buffer

    @abstractmethod
    def process(self) -> Dict[str, Any]:
        """
        The main method that orchestrates the report processing logic.

        This method must be implemented by all subclasses. Its responsibility
        is to use the appropriate Adapter and Repositories to process the
        data from the source file and persist it.
        """
        raise NotImplementedError('Subclasses must implement the "process" method.')
