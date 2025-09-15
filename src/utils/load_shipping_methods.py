import json
from pathlib import Path

from django.conf import settings

SHIPPING_METHODS_FILE: Path = settings.DATA_DIR / 'shipping_methods.json'


def load_shipping_methods() -> dict[str, str]:
    with open(SHIPPING_METHODS_FILE, 'r', encoding='utf-8') as f:
        return json.load(f)


def get_allowed_shipping_values() -> set[str]:
    data = load_shipping_methods()
    return set(data.values())


def get_shipping_choices() -> list[tuple[str, str]]:
    allowed_values = get_allowed_shipping_values()
    return [(val, val.title()) for val in sorted(allowed_values)]
