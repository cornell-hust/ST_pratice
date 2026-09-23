"""公平性（FAIR）对照用例：同组内不同表达方式的通过率差异量化。

每组两条用例独立按 n_runs 采样判定，通过率差异超过阈值即报告表达方式劣势。
阈值 2/3、1/3 由基线数据标定后固定（详见测试报告）。
"""

import pytest

from ledger import load_all
from nl2cron import translate
from oracle import semantic_equal

FAIR_MIN_RATE = 2 / 3
FAIR_MAX_GAP = 1 / 3

# 通过率是 k/n 的浮点商，差值比较会引入一个 ulp 级误差：1 - 2/3 得
# 0.33333333333333337，比 1/3 略大，恰好卡在阈值上时会误报不公平。
# 用一个小容差吸收，判定语义不变（通过率本身是离散的 k/n）。
EPS = 1e-9


def _fair_groups():
    groups: dict[str, list[dict]] = {}
    for case in load_all():
        if case["dimension"] == "fairness":
            groups.setdefault(case["group"], []).append(case)
    return dict(sorted(groups.items()))


FAIR_GROUPS = _fair_groups()


def _run_ok(case, run: int) -> bool:
    """单次采样判定：无组件错误、过结构守卫、与参考表达式语义等价。"""
    result = translate(case["input"], run=run)
    if result.error is not None or not result.valid:
        return False
    return semantic_equal(
        result.cron, case["reference_cron"], case["windows"], case.get("tz")
    )


@pytest.mark.fairness
@pytest.mark.parametrize("group_name", list(FAIR_GROUPS), ids=list(FAIR_GROUPS))
def test_fair_group(group_name):
    cases = FAIR_GROUPS[group_name]
    rates = {}
    for case in cases:
        outcomes = [_run_ok(case, run) for run in range(case["n_runs"])]
        rates[case["id"]] = sum(outcomes) / case["n_runs"]
    gap = max(rates.values()) - min(rates.values())
    assert min(rates.values()) >= FAIR_MIN_RATE - EPS, (
        f"{group_name} 存在表达方式劣势: 通过率 {rates}（阈值 {FAIR_MIN_RATE:.2f}）"
    )
    assert gap <= FAIR_MAX_GAP + EPS, (
        f"{group_name} 组内通过率差距过大: {rates}（差距 {gap:.2f} > {FAIR_MAX_GAP:.2f}）"
    )
