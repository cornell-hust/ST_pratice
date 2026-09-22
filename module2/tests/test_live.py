"""真实 API 冒烟用例（仅在 LIVE=1 时运行，平时自动跳过）。"""

import pytest

from checks import check_reference
from nl2cron import replay

SMOKE_CASE = {
    "id": "AI-LIVE-001",
    "input": "每小时整点运行一次",
    "reference_cron": "0 * * * *",
    "windows": ["2024-03-11T00:00:00", "2024-11-02T00:00:00"],
    "tz": None,
    "n_runs": 1,
}


@pytest.mark.live
def test_live_smoke():
    if not replay.live_mode():
        pytest.skip("回放模式：设置 LIVE=1 并配置 NL2CRON_API_KEY 后运行真实冒烟")
    check_reference(SMOKE_CASE)
