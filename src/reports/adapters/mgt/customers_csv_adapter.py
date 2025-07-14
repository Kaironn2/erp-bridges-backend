import pandas as pd

from mgt.schemas.customers_report_schema import CustomerReportData
from reports.adapters.base_adapter import BaseReportAdapter


class MgtCustomersCsvAdapter(BaseReportAdapter[CustomerReportData]):
    """
    read, clean, structures and valid the data
    of csv customers report from mgt source
    """

    def __init__(self, file_path_or_buffer: str):
        super().__init__(file_path_or_buffer)

    def load_raw_data_to_df(self, file_path_or_buffer):
        try:
            df = pd.read_csv(file_path_or_buffer, sep=';', dtype=str)
            return df.fillna('')
        except Exception as e:
            print(f'Teste {e}')

    class Meta:
        datetime_columns = ['Cliente Desde']
        date_format = '%d/%m/%Y %H:%M:%S'
        keep_only_digits_columns = ['Telefone']
        lower_case_columns = ['Nome', 'E-mail', 'Grupo', 'Estado', 'País']
