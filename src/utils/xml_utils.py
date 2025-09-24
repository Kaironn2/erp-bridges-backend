from pathlib import Path
from typing import Any

import xmltodict


def xml_parse(xml_file: str | Path) -> dict[str, Any]:
    with open(xml_file, 'rb') as file:
        return xmltodict.parse(file)
