import pandas as pd

from mgt.schemas.buy_orders_report_schema import BuyOrderReportData
from reports.adapters.base_adapter import BaseReportAdapter


class MgtBuyOrdersCsvAdapter(BaseReportAdapter[BuyOrderReportData]):
    """
    This adapter read, clean, structures and valid the data
    of csv buy orders report from mgt source
    """
    def __init__(self, file_path_or_buffer: str):
        self.file_path_or_buffer = file_path_or_buffer

    def load_raw_data_to_df(self, file_path_or_buffer):
        try:
            self.df = pd.read_csv(self.file_path, sep=';', dtype=str)
            self.df.fillna('', inplace=True)
        except FileNotFoundError:
            raise ValueError(f'File not found in the path: {self.file_path}')
        except Exception as e:
            raise ValueError(f'Error on read csv file: {e}')

    class Meta:
        currency_columns = ['Frete', 'Desconto', 'Total da Venda']
        datetime_columns = ['Comprado Em']
        date_format = '%d/%m/%Y %H:%M:%S'
        keep_only_digits_columns = ['Número CPF/CNPJ', 'Shipping Telephone']
        lower_case_columns = [
            'Firstname', 'Lastname', 'Email', 'Grupo do Cliente', 'Payment Type'
        ]
        columns_to_replace_values = {
            'Payment Type': {
                'pix': 'pix',
                'cartão': 'cartão de crédito',
                'boleto': 'boleto bancário',
                'necessário': 'saldo',
            }
        }
