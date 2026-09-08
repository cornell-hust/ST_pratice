import json
import sys
from pathlib import Path
import pytest

MODULE_ROOT = Path(__file__).parents[1]
SUBJECT_ROOT = MODULE_ROOT / 'subject'
sys.path.insert(0, str(SUBJECT_ROOT))
CASES = json.loads((MODULE_ROOT / 'testdata' / 'cron_cases.json').read_text())
@pytest.fixture
def base_dt():
    from datetime import datetime, timezone
    return datetime(2024, 1, 15, 12, 0, tzinfo=timezone.utc)
