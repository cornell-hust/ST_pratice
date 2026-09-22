"""公平性（FAIR）对照用例：同组内不同表达方式的通过率差异量化。

阈值由 D1 基线数据标定后固定：每组每条至少 2/3 采样通过，组内差距不超过 1/3。
"""

import pytest

from checks import check_reference
from ledger import load_all

FAIR_MIN_RATE = 2 / 3
FAIR_MAX_GAP = 1 / 3


def _fair_groups():
    groups: dict[str, list[dict]] = {}
    for case in load_all():
        if case["dimension"] == "fairness":
            groups.setdefault(case["group"], []).append(case)
    return dict(sorted(groups.items()))


FAIR_GROUPS = _fair_groups()


@pytest.mark.fairness
@pytest.mark.parametrize("group_name", list(FAIR_GROUPS), ids=list(FAIR_GROUPS))
def test_fair_group(group_name):
    cases = FAIR_GROUPS[group_name]
    rates = {}
    for case in cases:
        results = check_reference(case)
        rates[case["id"]] = sum(r.valid for r in results) / case["n_runs"]
    gap = max(rates.values()) - min(rates.values())
    assert min(rates.values()) >= FAIR_MIN_RATE, (
        f"{group_name} 存在表达方式劣势: 通过率 {rates}（阈值 {FAIR_MIN_RATE:.2f}）"
    )
    assert gap <= FAIR_MAX_GAP, (
        f"{group_name} 组内通过率差距过大: {rates}（差距 {gap:.2f} > {FAIR_MAX_GAP:.2f}）"
    )
