from io import BytesIO, StringIO
from pathlib import Path
from typing import Union

FilePathLike = Union[str, Path]
ReadCsvBuffer = Union[BytesIO, StringIO]
CsvSource = Union[FilePathLike, ReadCsvBuffer]
