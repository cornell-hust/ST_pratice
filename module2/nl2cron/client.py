"""OpenAI 兼容 Chat Completions 客户端（标准库实现，零第三方依赖）。

通过环境变量适配任一产业模型服务商：
- NL2CRON_API_KEY   必填（LIVE 调用时）
- NL2CRON_BASE_URL  默认智谱 open.bigmodel.cn，可换 Z.ai / DeepSeek / Kimi 等
- NL2CRON_MODEL     默认 glm-4-flash
"""

import json
import os
import urllib.error
import urllib.request
from pathlib import Path

DEFAULT_BASE_URL = "https://open.bigmodel.cn/api/paas/v4"
DEFAULT_MODEL = "glm-4-flash"

# 备选密钥文件：不进 Git（.gitignore 已覆盖），避免密钥进入对话与提交历史
KEY_FILE = Path(__file__).resolve().parent.parent / ".api-key"


class LLMError(RuntimeError):
    """LLM 调用失败（网络/HTTP/响应结构）。"""


def current_model() -> str:
    return os.environ.get("NL2CRON_MODEL", DEFAULT_MODEL)


def _api_key() -> str | None:
    key = os.environ.get("NL2CRON_API_KEY")
    if key:
        return key.strip()
    if KEY_FILE.exists():
        return KEY_FILE.read_text(encoding="utf-8").strip() or None
    return None


def chat_completion(messages, *, temperature=0.0, timeout=60):
    """发起一次 chat/completions 调用，返回助手回复文本。"""
    api_key = _api_key()
    if not api_key:
        raise LLMError(
            "缺少 API Key：请设置环境变量 NL2CRON_API_KEY，或把密钥写入 "
            "module2/.api-key 文件（已 gitignore）。回放模式不需要密钥。"
        )
    base_url = os.environ.get("NL2CRON_BASE_URL", DEFAULT_BASE_URL).rstrip("/")
    model = current_model()
    payload = {"model": model, "messages": messages, "temperature": temperature}
    request = urllib.request.Request(
        base_url + "/chat/completions",
        data=json.dumps(payload, ensure_ascii=False).encode("utf-8"),
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {api_key}",
        },
        method="POST",
    )
    try:
        with urllib.request.urlopen(request, timeout=timeout) as response:
            data = json.loads(response.read().decode("utf-8"))
    except urllib.error.HTTPError as exc:
        detail = exc.read().decode("utf-8", "replace")[:300]
        raise LLMError(f"API HTTP {exc.code}: {detail}") from exc
    except urllib.error.URLError as exc:
        raise LLMError(f"API 连接失败: {exc.reason}") from exc
    try:
        return data["choices"][0]["message"]["content"]
    except (KeyError, IndexError, TypeError) as exc:
        raise LLMError(
            "API 响应结构异常: " + json.dumps(data, ensure_ascii=False)[:300]
        ) from exc
