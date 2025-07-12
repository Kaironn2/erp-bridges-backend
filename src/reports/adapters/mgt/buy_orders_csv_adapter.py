import pandas as pd

from mgt.schemas.buy_orders_report_schema import BuyOrderReportData
from reports.adapters.base_adapter import BaseReportAdapter


class MgtBuyOrdersCsvAdapter(BaseReportAdapter[BuyOrderReportData]):
    """
    read, clean, structures and valid the data
    of csv buy orders report from mgt source
    """
    def __init__(self, file_path_or_buffer: str):
        super().__init__(file_path_or_buffer)

    def load_raw_data_to_df(self, file_path_or_buffer):
        try:
            df = pd.read_csv(file_path_or_buffer, sep=';', dtype=str)
            return df.fillna('')
        except FileNotFoundError:
            raise ValueError(f'File not found in the path: {file_path_or_buffer}')
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
        columns_mapping = {
            'Payment Type': {
                'pix': 'pix',
                'cartão': 'cartão de crédito',
                'boleto': 'boleto bancário',
                'necessário': 'saldo',
            }
        }
        mapping_contains = True
