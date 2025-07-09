import pandas as pd


class MgtBuyOrdersCsvAdapter:
    """
    This adapter read, clean, structures and valid the data
    of csv buy orders report from mgt source
    """
    def __init__(self, file_path: str):
        self.file_path = file_path
        self._read_csv()

    def _read_csv(self):
        try:
            self.df = pd.read_csv(self.file_path, sep=';', dtype=str)
            self.df.fillna('', inplace=True)
        except FileNotFoundError:
            raise ValueError(f'File not found in the path: {self.file_path}')
        except Exception as e:
            raise ValueError(f'Error on read csv file: {e}')

    def process(self):
        ...     # TODO - implement data clean and transform
