import pytest
from pathlib import Path
from django.conf import settings


@pytest.fixture
def mgt_fixtures_path() -> Path:
    """Returns mgt fixtures path"""
    return Path(settings.BASE_DIR) / 'mgt' / 'tests' / 'fixtures'
