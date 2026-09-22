# testdata/ — 用例账本与录制回放缓存

| 文件/目录 | 作用 |
| --- | --- |
| `nl2cron_cases.json` | **用例单一数据源（账本）**：36 条用例的输入、参考表达式、时间窗、维度与方法标注 |
| `recordings/` | LLM 响应录制缓存：`<sha256>.json` 一文件一次调用，`index.jsonl` 为人读索引 |

## 约定

- pytest 与演示脚本都从账本取数，**不硬编码用例**；
- `recordings/` **入 Git**：保证评委无 API Key 也能离线复现全部用例（回放模式）；
- 重新录制：`LIVE=1 python tools/record_responses.py`（需 `NL2CRON_API_KEY`），已有录制默认跳过，`--force` 覆盖；
- 录制键 = sha256(提示词版本, 模型, 输入, run 序号)，因此 v1/v2 提示词、不同模型的响应互不覆盖——这正是"切换被测版本暴露缺陷"的基线对照机制。
