from pathlib import Path
from typing import Any, Union
import pandas as pd

from core.ingestion.base_extractor import BaseExtractor
from utils.xml_utils import xml_parse


class InvoiceXmlExtractor(BaseExtractor):
    def __init__(self, xml_files: Union[str, Path, list[Union[str, Path]]]) -> None:
        if isinstance(xml_files, (str, Path)):
            self.xml_files = [xml_files]
        else:
            self.xml_files = xml_files

    def extract(self) -> pd.DataFrame:
        all_data = []

        for file_path in self.xml_files:
            xml_dict = self._load_xml(file_path)
            mapped_data = self._map_invoice_data(xml_dict)
            all_data.append(mapped_data)

        return pd.DataFrame(all_data)

    def _load_xml(self, file_path: Union[str, Path]) -> dict[str, Any]:
        try:
            return xml_parse(file_path)
        except FileNotFoundError:
            raise ValueError(f'File not found in the path: {file_path}')
        except Exception as e:
            raise ValueError(f'Error reading xml file {file_path}: {e}')

    def _map_invoice_data(self, xml: dict[str, Any]) -> dict[str, Any]:
        infNFe = xml['nfeProc']['NFe']['infNFe']
        ide = infNFe['ide']
        recipient = infNFe.get('entrega', {})

        invoice_data = {
            'access_key': infNFe['@Id'].replace('NFe', ''),
            'number': ide.get('nNF'),
            'operation_nature': ide.get('natOp'),
            'cfop': infNFe['det'][0]['prod'].get('CFOP'),
            'issue_date': pd.to_datetime(ide.get('dhEmi')).date(),
            'shipping_amount': float(infNFe['total']['ICMSTot'].get('vFrete', 0)),
            'total_amount': float(infNFe['total']['ICMSTot'].get('vNF', 0)),
        }

        recipient_data = {
            'cpf': recipient.get('CPF'),
            'name': recipient.get('xNome'),
            'street': recipient.get('enderDest', {}).get('xLgr'),
            'number': recipient.get('enderDest', {}).get('nro'),
            'complement': recipient.get('enderDest', {}).get('xCpl'),
            'neighborhood': recipient.get('enderDest', {}).get('xBairro'),
            'city': recipient.get('enderDest', {}).get('xMun'),
            'state': recipient.get('enderDest', {}).get('UF'),
            'zip_code': recipient.get('enderDest', {}).get('CEP'),
            'country': recipient.get('enderDest', {}).get('xPais'),
            'phone': recipient.get('enderDest', {}).get('fone'),
            'email': recipient.get('email'),
        }

        return {**invoice_data, **recipient_data}
