import pytest
from pathlib import Path
from django.conf import settings


@pytest.fixture
def ecs_fixtures_path() -> Path:
    """Returns ecs fixtures path"""
    return Path(settings.BASE_DIR) / 'ecs' / 'tests' / 'fixtures'
