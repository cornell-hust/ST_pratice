"""translate() —— 被测入口：LLM 调用 + JSON 提取 + 最小输出守卫。

v1 的守卫只做"取 JSON、取 cron、可解析"三件事；守卫与提示词的加固都在 v2。
"""

import json
import os
import re
from dataclasses import dataclass

from . import deps  # noqa: F401  确保 croniter（module1/subject 快照）可导入
from croniter import croniter

from . import replay
from .client import chat_completion, current_model
from .prompts import DEFAULT_PROMPT_VERSION, PROMPTS

_JSON_BRACES = re.compile(r"\{.*\}", re.S)


@dataclass
class TranslateResult:
    text: str
    prompt_version: str
    raw: str            # 模型原始输出（缺陷证据）
    cron: str | None    # 提取出的 cron 表达式（未通过守卫时原样保留，供取证）
    explanation: str
    valid: bool         # 结构守卫结论：5 字段且 croniter 可解析
    error: str | None   # 解析/格式错误信息；None 表示输出形态合法


def _parse(content: str):
    """从模型输出提取 {cron, explanation}；返回 (cron, explanation, error)。"""
    match = _JSON_BRACES.search(content)
    if not match:
        return None, "", "输出中找不到 JSON 对象"
    try:
        data = json.loads(match.group(0))
    except json.JSONDecodeError as exc:
        return None, "", f"JSON 解析失败: {exc}"
    if not isinstance(data, dict):
        return None, "", "JSON 不是对象"
    cron = data.get("cron")
    if isinstance(cron, str):
        cron = cron.strip() or None
    elif cron is not None:
        cron = str(cron).strip() or None
    explanation = str(data.get("explanation", ""))
    return cron, explanation, None


def _guard_valid(cron) -> bool:
    """结构守卫：恰好 5 个空白分隔字段，且 croniter 认可。"""
    if not cron:
        return False
    if len(cron.split()) != 5:
        return False
    return bool(croniter.is_valid(cron))


def translate(
    text: str,
    *,
    run: int = 0,
    prompt_version: str | None = None,
    live: bool | None = None,
) -> TranslateResult:
    """把一段自然语言调度描述转成 cron 表达式。

    run：同一输入的第几次采样（用于非确定性统计；录制时每次采样单独缓存）。
    prompt_version/live：默认读环境变量 NL2CRON_PROMPT_VERSION / LIVE。
    """
    version = prompt_version or os.environ.get(
        "NL2CRON_PROMPT_VERSION", DEFAULT_PROMPT_VERSION
    )
    if version not in PROMPTS:
        raise ValueError(f"未知提示词版本: {version}（可选 {sorted(PROMPTS)}）")
    model = current_model()
    key = replay.cache_key(version, model, text, run)
    is_live = replay.live_mode() if live is None else live
    if is_live:
        messages = [
            {"role": "system", "content": PROMPTS[version]},
            {"role": "user", "content": text},
        ]
        content = chat_completion(messages, temperature=0.0)
        replay.record(
            key, prompt_version=version, model=model, text=text, run=run, content=content
        )
    else:
        content = replay.replay(key)

    cron, explanation, error = _parse(content)
    valid = error is None and _guard_valid(cron)
    if error is None and cron is not None and not valid:
        error = "cron 未通过结构守卫（需恰好 5 字段且 croniter 可解析）"
    return TranslateResult(
        text=text,
        prompt_version=version,
        raw=content,
        cron=cron,
        explanation=explanation,
        valid=valid,
        error=error,
    )
