# 模块二：AI 融合实践（方案 1 —— 测 AI）

本目录保存模块二全部材料。**方案选择：测 AI（测试对象含 AI 模型）**——在模块一的
`croniter` 定时表达式库之上添加 LLM 组件 `nl2cron`（自然语言 → 标准 5 字段 cron 表达式），
针对它开展鲁棒性、公平性、安全性测试。

> 选择理由：课程录音明确"AI 应当是辅助者而非替代者"；本方案中 AI 组件是被测对象，
> 测试设计、结果判定与质量结论始终由人完成。croniter 同时充当 LLM 输出的确定性
> oracle 裁判——这是"给 AI 组件建立可自动化判定标准"的关键设计。

## 目录约定

```text
module2/
├── nl2cron/                         # 被测 AI 组件（提示词 v1 基线 / v2 修复版，演进留痕）
├── tests/                           # 三层 oracle 自动化测试（结构/语义/安全）
├── testdata/
│   ├── nl2cron_cases.json           # 40 条用例账本（单一数据源）
│   ├── recordings/                  # LLM 响应录制缓存（入 Git，离线可复现）
│   ├── execution_summary.json       # 执行汇总（summarize.py 生成）
│   └── execution_report.md          # 维度统计报告（报告/PPT 数字来源）
├── testcases/                       # 附录一：测试用例清单
├── defects/                         # 缺陷清单与复现证据
├── reports/                         # 附录四：测试报告（模块二）
├── presentation/                    # 成果汇报 PPT、演示视频与现场演示脚本
├── tools/                           # 录制器 / 汇总器 / 清单生成器
├── ai-usage/                        # AI 使用披露（调研纪要、关键决策日志）
├── requirements_traceability.md     # 需求 → 用例 → 实现 → 缺陷 追踪矩阵
├── pytest.ini / requirements-dev.txt / README.md
```

## 环境与运行

Python 3.10+。测试默认**回放模式**：离线、确定性、零成本，不需要 API Key。

```bash
python -m venv .venv
source .venv/bin/activate          # Windows：.venv/Scripts/activate
python -m pip install -r requirements-dev.txt
python -m pytest -q                # 期望：全部通过（结果回填后更新本行）
```

### 录制与回放（非确定性处理）

| 命令 | 作用 |
| --- | --- |
| `LIVE=1 python tools/record_responses.py` | 真实调用 LLM API 并录制响应（需密钥，见下） |
| `python -m pytest -q` | 回放录制响应，任何人可离线复现同一结果 |
| `NL2CRON_PROMPT_VERSION=v1 python -m pytest -q` | 切到基线提示词：缺陷用例原形毕露 |
| `NL2CRON_PROMPT_VERSION=v2 python -m pytest -q` | 修复后提示词：全部通过 |

API Key 配置（仅录制时需要）：环境变量 `NL2CRON_API_KEY`，或写入 `module2/.api-key`
文件（已被 .gitignore 覆盖）。服务商经 `NL2CRON_BASE_URL` / `NL2CRON_MODEL` 适配任一
OpenAI 兼容端点（智谱 / Z.ai / DeepSeek / Kimi 等）。

## 测试设计速览

- **三层 oracle**：结构层（5 字段 + 无 Quartz 方言）→ 语义层（与参考表达式在月末/闰年/
  DST/跨年多时间窗的触发序列逐点比对，Spider 式执行准确率）→ 安全层（金丝雀泄露 +
  注入劫持检测）。
- **用例分布（40 条）**：功能语义 MFT 12（等价类/边界值/场景法）、鲁棒性 INV 10（同义
  改写/错别字/零宽字符/无关输入/超长）、方向性 DIR 4（蜕变测试）、安全性 SAF 6（OWASP
  LLM Top 10 映射）、公平性 FAIR 4 组 8 条（中英/语域/数字体系对照）。
- **非确定性**：temperature=0 下核心用例 n=3 采样统计一致率（Ouyang et al., TOSEM：
  T=0 也不保证确定）。
- **方法依据**：CheckList（Ribeiro et al., ACL 2020）、执行式 oracle（Spider，EMNLP 2018）、
  garak/OWASP 安全分类、跨语言公平性（Hofmann et al., Nature 2024）——详见
  `ai-usage/调研纪要/`。

## 缺陷闭环

`nl2cron` 提示词 v1 刻意从简，暴露真实缺陷；v2 为修复版。缺陷以
`NL2C_PROMPT_VERSION=v1` 复现、`v2` 回归验证，与模块一"baseline/subject 切换"的演示
方式同构。缺陷清单见 `defects/`（执行后回填）。

## 交付物

| 附录 | 交付物 | 位置 |
| --- | --- | --- |
| 附录一 | 测试用例清单（40 条 AI 用例） | `testcases/测试用例清单（模块二）.xlsx` |
| — | 缺陷清单（录音口径：无需单独缺陷报告） | `defects/缺陷清单（模块二）.docx` |
| 附录四 | 测试报告（模块二） | `reports/测试报告（模块二）.docx` |
| — | 成果汇报 PPT | `presentation/模块二成果汇报.pptx` |
| — | 演示视频 | `presentation/模块二演示视频.mp4` |
| — | AI 使用披露 | `ai-usage/` |
