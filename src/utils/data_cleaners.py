import re


def remove_non_digits(value: str) -> str:
    if value:
        return re.sub(r'\D', '', value)
    return value
