#!/usr/bin/env python
"""离线演示：自然语言 → cron 翻译 + oracle 判定（回放模式，无需网络与 API Key）。

用法（module2 目录下）：
    .venv/bin/python presentation/演示-离线复现.py "每天早上九点"
    .venv/bin/python presentation/演示-离线复现.py --case AI-UT-001
    NL2CRON_PROMPT_VERSION=v1 .venv/bin/python presentation/演示-离线复现.py --case AI-UT-021

输入不在录制缓存中时会提示先用 record_responses.py 录制；
切换 NL2CRON_PROMPT_VERSION 可对比基线/修复后的行为（缺陷复现演示）。
"""

import argparse
import sys
from pathlib import Path

MODULE2_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(MODULE2_ROOT))
sys.path.insert(0, str(MODULE2_ROOT / "tests"))

from ledger import load_all  # noqa: E402
from nl2cron import translate  # noqa: E402
from nl2cron.client import current_model  # noqa: E402
from nl2cron.prompts import DEFAULT_PROMPT_VERSION  # noqa: E402
from oracle import safety_violation, semantic_equal  # noqa: E402


def show(text, reference=None, windows=None, tz=None, attacker_target=None) -> None:
    result = translate(text)
    print(f"输入：{text}")
    print(f"模型原始输出：{result.raw!r}")
    if result.error:
        print(f"✗ 组件错误：{result.error}")
        return
    print(f"解析：cron={result.cron!r}  守卫={'通过' if result.valid else '未通过'}")
    print(f"解释：{result.explanation}")
    if reference:
        equal = semantic_equal(result.cron, reference, windows, tz)
        print(f"oracle：期望 {reference!r} → {'✓ 语义等价' if equal else '✗ 语义不等价'}")
    violation = safety_violation(result, attacker_target)
    if violation:
        print(f"oracle：✗ 安全违规 —— {violation}")


def main() -> int:
    parser = argparse.ArgumentParser(description="NL→cron 离线演示（回放模式）")
    parser.add_argument("text", nargs="?", help="自然语言调度描述")
    parser.add_argument("--case", help="用例编号，如 AI-UT-001（自动带参考答案判定）")
    args = parser.parse_args()

    version = __import__("os").environ.get(
        "NL2CRON_PROMPT_VERSION", DEFAULT_PROMPT_VERSION
    )
    print(f"[提示词 {version}｜模型 {current_model()}｜回放模式]\n")

    if args.case:
        matched = [c for c in load_all() if c["id"] == args.case]
        if not matched:
            print(f"账本中没有 {args.case}", file=sys.stderr)
            return 2
        case = matched[0]
        show(
            case["input"],
            case.get("reference_cron"),
            case.get("windows"),
            case.get("tz"),
            case.get("attacker_target"),
        )
        return 0

    if not args.text:
        parser.error("请提供自然语言文本或 --case 用例编号")
    show(args.text)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
