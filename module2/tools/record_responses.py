#!/usr/bin/env python
"""录制器：遍历用例账本，真实调用 LLM API 并把响应写入 testdata/recordings/。

用法（在 module2/ 目录下，先配置环境变量）：
    export NL2CRON_API_KEY=你的密钥          # 必填
    export NL2CRON_BASE_URL=...             # 可选，默认智谱 open.bigmodel.cn
    export NL2CRON_MODEL=...                # 可选，默认 glm-4-flash
    export NL2CRON_PROMPT_VERSION=v1        # 可选，默认 v1
    LIVE=1 .venv/bin/python tools/record_responses.py [--force]

--force：已存在的录制也重新调用覆盖（默认跳过已有录制，节省费用）。
录制完成后直接 `python -m pytest -q` 即可离线回放全部用例。
"""

import argparse
import json
import sys
import time
from pathlib import Path

MODULE2_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(MODULE2_ROOT))
sys.path.insert(0, str(MODULE2_ROOT / "tests"))

from ledger import load_all  # noqa: E402
from nl2cron import replay  # noqa: E402
from nl2cron.client import LLMError, current_model  # noqa: E402
from nl2cron.prompts import PROMPTS  # noqa: E402
from nl2cron.translator import translate  # noqa: E402


def main() -> int:
    parser = argparse.ArgumentParser(description="录制 LLM 响应供离线回放")
    parser.add_argument("--force", action="store_true", help="覆盖已存在的录制")
    parser.add_argument("--sleep", type=float, default=0.5, help="调用间隔秒数")
    args = parser.parse_args()

    version = __import__("os").environ.get(
        "NL2CRON_PROMPT_VERSION",
        __import__("nl2cron.prompts", fromlist=["DEFAULT_PROMPT_VERSION"]).DEFAULT_PROMPT_VERSION,
    )
    model = current_model()
    cases = load_all()
    tasks = [
        (case, run)
        for case in cases
        for run in range(case["n_runs"])
    ]
    print(
        f"录制计划：{len(cases)} 条用例，共 {len(tasks)} 次调用"
        f"（提示词 {version}，模型 {model}）"
    )
    if version not in PROMPTS:
        print(f"错误：未知提示词版本 {version}", file=sys.stderr)
        return 2

    done = skipped = failed = 0
    for index, (case, run) in enumerate(tasks, 1):
        key = replay.cache_key(version, model, case["input"], run)
        if not args.force and (replay.RECORDINGS_DIR / f"{key}.json").exists():
            skipped += 1
            continue
        try:
            translate(case["input"], run=run, prompt_version=version, live=True)
        except LLMError as exc:
            failed += 1
            print(f"[{index}/{len(tasks)}] {case['id']} run{run} 失败: {exc}", file=sys.stderr)
        else:
            done += 1
        time.sleep(args.sleep)
        if index % 10 == 0:
            print(f"进度 {index}/{len(tasks)}（新增 {done}，跳过 {skipped}，失败 {failed}）")

    print(f"完成：新增 {done}，跳过 {skipped}，失败 {failed}")
    if failed:
        print("存在失败调用，可重跑本命令续录（已有录制会自动跳过）。", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
