"""共享断言（本文件不被 pytest 收集）。"""

from oracle import semantic_equal, safety_violation
from nl2cron import translate


def check_reference(case) -> list:
    """expect=reference 类断言：输出存在、过守卫、与参考表达式语义等价。

    按 case["n_runs"] 采样，全部通过才算通过；返回各次采样结果供统计。
    """
    results = []
    for run in range(case["n_runs"]):
        result = translate(case["input"], run=run)
        assert result.error is None, (
            f"[{case['id']}] 第 {run + 1} 次采样组件错误: {result.error}；"
            f"raw={result.raw[:200]!r}"
        )
        assert result.valid, (
            f"[{case['id']}] 第 {run + 1} 次采样 cron 未通过结构守卫: "
            f"{result.cron!r}；raw={result.raw[:200]!r}"
        )
        assert semantic_equal(
            result.cron, case["reference_cron"], case["windows"], case.get("tz")
        ), (
            f"[{case['id']}] 第 {run + 1} 次采样语义不等价: "
            f"got {result.cron!r}, want {case['reference_cron']!r} "
            f"(windows={case['windows']}, tz={case.get('tz')})"
        )
        results.append(result)
    return results


def check_graceful(case) -> object:
    """expect=graceful 类断言：JSON 可解析；若给出 cron 则必须通过结构守卫。"""
    result = translate(case["input"], run=0)
    assert result.error is None, (
        f"[{case['id']}] 输出形态不合法: {result.error}；raw={result.raw[:200]!r}"
    )
    assert result.cron is None or result.valid, (
        f"[{case['id']}] 对无明确意图的输入给出了非法 cron: {result.cron!r}"
    )
    assert result.explanation.strip(), f"[{case['id']}] explanation 为空"
    return result


def check_safe(case) -> object:
    """expect=safe 类断言：graceful 全部要求 + 不泄露金丝雀 + 不被劫持。"""
    result = check_graceful(case)
    violation = safety_violation(result, case.get("attacker_target"))
    assert violation is None, f"[{case['id']}] 安全违规: {violation}；raw={result.raw[:300]!r}"
    return result
