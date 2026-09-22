"""用例账本加载助手（本文件不被 pytest 收集）。"""

import json
from pathlib import Path

LEDGER_PATH = Path(__file__).resolve().parents[1] / "testdata" / "nl2cron_cases.json"


def load_all() -> list[dict]:
    data = json.loads(LEDGER_PATH.read_text(encoding="utf-8"))
    return data["cases"]


def of_dimension(dimension: str) -> list[dict]:
    return [case for case in load_all() if case["dimension"] == dimension]


def ids(cases: list[dict]) -> list[str]:
    return [case["id"] for case in cases]
