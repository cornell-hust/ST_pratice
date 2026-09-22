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

DEFAULT_BASE_URL = "https://open.bigmodel.cn/api/paas/v4"
DEFAULT_MODEL = "glm-4-flash"


class LLMError(RuntimeError):
    """LLM 调用失败（网络/HTTP/响应结构）。"""


def current_model() -> str:
    return os.environ.get("NL2CRON_MODEL", DEFAULT_MODEL)


def chat_completion(messages, *, temperature=0.0, timeout=60):
    """发起一次 chat/completions 调用，返回助手回复文本。"""
    api_key = os.environ.get("NL2CRON_API_KEY")
    if not api_key:
        raise LLMError(
            "缺少环境变量 NL2CRON_API_KEY。回放模式不需要它；"
            "录制（LIVE=1）前请先配置 API Key。"
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
