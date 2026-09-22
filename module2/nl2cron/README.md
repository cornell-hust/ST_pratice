# nl2cron/ — 被测 AI 组件（自然语言 → cron 表达式）

模块二在模块一 croniter 之上添加的 LLM 组件，约 150 行：

| 文件 | 职责 |
| --- | --- |
| `translator.py` | 被测入口 `translate(text) -> TranslateResult`：LLM 调用 + JSON 提取 + 最小输出守卫 |
| `prompts.py` | 系统提示词 v1（基线，刻意从简）与 v2（缺陷修复版），`NL2CRON_PROMPT_VERSION` 切换 |
| `client.py` | OpenAI 兼容 Chat Completions 客户端（纯标准库，零第三方依赖） |
| `replay.py` | 响应录制/回放缓存，保证离线确定性复现 |
| `deps.py` | croniter 依赖注入（复用 `module1/subject` 快照） |

## 环境变量（仅 LIVE 录制时需要）

| 变量 | 默认 | 说明 |
| --- | --- | --- |
| `NL2CRON_API_KEY` | 无 | API 密钥（回放模式不需要） |
| `NL2CRON_BASE_URL` | `https://open.bigmodel.cn/api/paas/v4` | 任一 OpenAI 兼容端点（Z.ai/DeepSeek/Kimi…） |
| `NL2CRON_MODEL` | `glm-4-flash` | 模型名 |
| `NL2CRON_PROMPT_VERSION` | `v1` | 提示词版本（`v1`=基线，`v2`=修复后） |
| `LIVE` | 未设置 | `=1` 时真实调用 API 并录制 |
