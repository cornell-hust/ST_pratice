import json
from pathlib import Path
import pytest

CASES = json.loads((Path(__file__).parents[1] / 'testdata' / 'cron_cases.json').read_text())
@pytest.fixture
def base_dt():
    from datetime import datetime, timezone
    return datetime(2024, 1, 15, 12, 0, tzinfo=timezone.utc)
