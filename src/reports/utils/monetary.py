from decimal import Decimal, InvalidOperation


def to_decimal(value: str) -> Decimal:
    """Converts str to Decimal object

    Args:
        value (str): str value

    Returns:
        Decimal: value converted to Decimal object
    """
    try:
        return Decimal(value)
    except (InvalidOperation, TypeError):
        return Decimal('0.00')
