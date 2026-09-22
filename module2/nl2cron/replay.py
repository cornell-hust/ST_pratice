"""API 响应的录制 / 回放缓存。

设计动机（也是模块二"AI 反思"的素材）：LLM 输出具有非确定性且依赖网络与密钥，
直接在 pytest 里打真实 API 会让"一键运行全部用例"依赖外部条件。因此：
- 录制：LIVE=1 时真实调用 API，把响应写入 testdata/recordings/<key>.json；
- 回放：默认模式只读录制文件，离线、确定、零成本，评委无需密钥即可复现全部用例；
- 缓存键 = sha256(提示词版本, 模型, 输入文本, run 序号)，提示词 v1/v2 的响应各存一份。
"""

import hashlib
import json
import os
from pathlib import Path

RECORDINGS_DIR = Path(__file__).resolve().parent.parent / "testdata" / "recordings"
INDEX_PATH = RECORDINGS_DIR / "index.jsonl"


def live_mode() -> bool:
    return os.environ.get("LIVE") == "1"


def cache_key(prompt_version: str, model: str, text: str, run: int) -> str:
    raw = json.dumps([prompt_version, model, text, run], ensure_ascii=False)
    return hashlib.sha256(raw.encode("utf-8")).hexdigest()[:24]


def record(key, *, prompt_version, model, text, run, content) -> None:
    RECORDINGS_DIR.mkdir(parents=True, exist_ok=True)
    payload = {
        "key": key,
        "prompt_version": prompt_version,
        "model": model,
        "input": text,
        "run": run,
        "content": content,
    }
    (RECORDINGS_DIR / f"{key}.json").write_text(
        json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    with INDEX_PATH.open("a", encoding="utf-8") as index:
        index.write(
            json.dumps(
                {k: payload[k] for k in ("key", "prompt_version", "model", "run", "input")},
                ensure_ascii=False,
            )
            + "\n"
        )


def replay(key: str) -> str:
    path = RECORDINGS_DIR / f"{key}.json"
    if not path.exists():
        raise FileNotFoundError(
            f"回放缓存缺失：{path.name}。请先配置 NL2CRON_API_KEY 后执行 "
            "LIVE=1 python tools/record_responses.py 生成录制，再运行测试。"
        )
    return json.loads(path.read_text(encoding="utf-8"))["content"]
