from datetime import datetime
from typing import Union

import pandas as pd
from django.utils.timezone import is_naive, make_aware
from pytz import timezone

SAO_PAULO = timezone('America/Sao_Paulo')


def local_to_aware(dt: Union[datetime, None]) -> Union[datetime, None]:
    """
    Convert naive datetime to timezone-aware (America/Sao_Paulo).
    Returns the original datetime if already aware, or None.
    """
    if dt is None:
        return None
    if pd.isna(dt):
        return dt
    if is_naive(dt):
        return make_aware(dt, timezone=SAO_PAULO)
    return dt
