import pytest
from pathlib import Path
from django.conf import settings


@pytest.fixture
def data_tests_folder() -> Path:
    """Returns data tests folder path"""
    return Path(settings.BASE_DIR) / 'reports' / 'ingestion' / 'tests' / 'fixtures'
