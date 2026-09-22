#!/usr/bin/env python
"""执行汇总器：回放模式下逐用例评估，产出执行结果统计。

用法（module2 目录下）：
    .venv/bin/python tools/summarize.py            # 提示词版本读环境变量，默认 v1

产出：
- testdata/execution_summary.json：逐用例结果（gen_case_list.py 用它回填清单）
- testdata/execution_report.md：按维度统计的执行报告（测试报告/PPT 数字来源）
"""

import json
import os
import sys
from collections import Counter, defaultdict
from datetime import datetime
from pathlib import Path

MODULE2_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(MODULE2_ROOT))
sys.path.insert(0, str(MODULE2_ROOT / "tests"))

from checks import check_graceful, check_reference, check_safe  # noqa: E402
from ledger import load_all  # noqa: E402
from nl2cron.client import current_model  # noqa: E402
from nl2cron.prompts import DEFAULT_PROMPT_VERSION  # noqa: E402
from nl2cron.translator import translate  # noqa: E402

CHECKS = {"reference": check_reference, "graceful": check_graceful, "safe": check_safe}

DIMENSION_NAMES = {
    "functional": "功能语义（MFT）",
    "robustness": "鲁棒性（INV）",
    "directional": "方向性蜕变（DIR）",
    "safety": "安全性（SAF）",
    "fairness": "公平性（FAIR）",
}


def short(result) -> str:
    cron = result.cron if result.cron is not None else "null"
    return f"cron={cron}；{result.explanation[:60]}"


def evaluate_case(case):
    """返回 (status, detail, results)；复用 tests/checks.py 的断言逻辑。"""
    try:
        results = CHECKS[case["expect"]](case)
        return "OK", short(results[0] if len(results) == 1 else results[-1]), results
    except AssertionError as exc:
        return "FAIL", str(exc)[:300], []


def main() -> int:
    version = os.environ.get("NL2CRON_PROMPT_VERSION", DEFAULT_PROMPT_VERSION)
    cases = load_all()
    summary = {
        "meta": {
            "prompt_version": version,
            "model": current_model(),
            "generated_at": datetime.now().isoformat(timespec="seconds"),
        },
        "cases": {},
    }
    by_dimension: dict[str, list[int]] = defaultdict(lambda: [0, 0])
    failures: list[str] = []

    for case in cases:
        status, detail, results = evaluate_case(case)
        entry = {
            "dimension": case["dimension"],
            "status": status,
            "result": detail,
            "n_runs": case["n_runs"],
        }
        if len(results) > 1:
            counts = max(Counter(r.cron for r in results).values())
            entry["agreement"] = counts / len(results)
        summary["cases"][case["id"]] = entry
        passed, total = by_dimension[case["dimension"]]
        by_dimension[case["dimension"]] = [passed + (status == "OK"), total + 1]
        if status == "FAIL":
            failures.append(case["id"])

    (MODULE2_ROOT / "testdata" / "execution_summary.json").write_text(
        json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8"
    )

    lines = [
        "# 模块二执行结果汇总",
        "",
        f"- 提示词版本：`{version}`｜模型：`{current_model()}`｜生成时间：{summary['meta']['generated_at']}",
        f"- 用例总数：{len(cases)}｜通过：{len(cases) - len(failures)}｜失败：{len(failures)}",
        "",
        "| 维度 | 通过/总数 | 通过率 |",
        "| --- | --- | --- |",
    ]
    for dimension, (passed, total) in by_dimension.items():
        rate = passed / total if total else 0
        lines.append(
            f"| {DIMENSION_NAMES.get(dimension, dimension)} | {passed}/{total} | {rate:.0%} |"
        )
    if failures:
        lines += ["", "## 失败用例", ""]
        lines += [f"- `{case_id}`：{summary['cases'][case_id]['result']}" for case_id in failures]
    (MODULE2_ROOT / "testdata" / "execution_report.md").write_text(
        "\n".join(lines) + "\n", encoding="utf-8"
    )

    print("\n".join(lines))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
