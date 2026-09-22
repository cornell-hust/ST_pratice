"""非确定性一致性统计：对 n_runs>1 的用例检查多次采样的字符串一致率。

这是"测 AI 与测传统软件不同"的直接证据（temperature=0 也不保证确定，
参见 Ouyang et al., TOSEM）。阈值 2/3 由基线数据标定。
"""

from collections import Counter

import pytest

from nl2cron import translate
from ledger import load_all

MIN_AGREEMENT = 2 / 3

REPEAT_CASES = [case for case in load_all() if case["n_runs"] > 1]


@pytest.mark.consistency
@pytest.mark.parametrize("case", REPEAT_CASES, ids=[case["id"] for case in REPEAT_CASES])
def test_run_agreement(case):
    crons = []
    for run in range(case["n_runs"]):
        result = translate(case["input"], run=run)
        assert result.error is None, f"[{case['id']}] 采样 {run + 1} 组件错误: {result.error}"
        crons.append(result.cron)
    agreement = max(Counter(crons).values()) / len(crons)
    assert agreement >= MIN_AGREEMENT, (
        f"[{case['id']}] {case['n_runs']} 次采样输出不一致（一致率 {agreement:.2f}）: {crons}"
    )
