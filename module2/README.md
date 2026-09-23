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
│   ├── execution_summary.json       # 执行汇总（summarize.py 生成，不入库）
│   └── execution_report.md          # 维度统计报告（报告/PPT 数字来源，不入库）
├── testcases/                       # 附录一：测试用例清单
├── defects/                         # 缺陷清单与复现证据
├── reports/                         # 附录四：测试报告（模块二）
├── presentation/                    # 成果汇报 PPT、演示视频与现场演示脚本
├── tools/                           # 汇总器 / 清单生成器 / 证据导出（录制器不入库，见下）
├── ai-usage/                        # AI 使用披露（调研纪要、关键决策日志）
├── requirements_traceability.md     # 需求 → 用例 → 实现 → 缺陷 追踪矩阵（本地保留，不入库）
├── pytest.ini / requirements-dev.txt / README.md
```

> 上表是**本地工作目录**的全貌；标「不入库」的与各子目录的素材稿、填充稿、制作过程材料
> 都保留在本地但不提交，实际入库范围见下文「入库范围」一节。

## 环境与运行

Python 3.10+。测试默认**回放模式**：离线、确定性、零成本，不需要 API Key。

```bash
python -m venv .venv
source .venv/bin/activate          # Windows：.venv/Scripts/activate
python -m pip install -r requirements-dev.txt
```

**录制缓存入库时用的模型是 `deepseek-flash`，而缓存键包含模型名**，所以回放要显式带上
`NL2CRON_MODEL`（`NL2CRON_BASE_URL` 只在 LIVE 录制时才会真正发起请求，回放无网络依赖）：

```bash
NL2CRON_MODEL=deepseek-flash NL2CRON_PROMPT_VERSION=v1 python -m pytest -q  # 11 失败：缺陷原形毕露
NL2CRON_MODEL=deepseek-flash NL2CRON_PROMPT_VERSION=v2 python -m pytest -q  # 82 通过：全部修复
```

> Windows 上还需 `pip install tzdata`：系统不带时区库，`zoneinfo` 会找不到
> `America/New_York`（已在 `requirements-dev.txt` 中声明）。

### 录制与回放（非确定性处理）

| 命令 | 作用 |
| --- | --- |
| `LIVE=1 python tools/record_responses.py` | 真实调用 LLM API 并录制响应（需密钥，见下）。该脚本为**本地文件、不入库**，重新录制需在本地工作目录执行 |
| `NL2CRON_MODEL=... python -m pytest -q` | 回放录制响应，任何人可离线复现同一结果 |
| `NL2CRON_PROMPT_VERSION=v1 ... python -m pytest -q` | 切到基线提示词：缺陷用例原形毕露 |
| `NL2CRON_PROMPT_VERSION=v2 ... python -m pytest -q` | 修复后提示词：全部通过 |

API Key 配置（仅录制时需要）：环境变量 `NL2CRON_API_KEY`，或写入 `module2/.api-key`
文件（已被 .gitignore 覆盖）。服务商经 `NL2CRON_BASE_URL` / `NL2CRON_MODEL` 适配任一
OpenAI 兼容端点（智谱 / Z.ai / DeepSeek / Kimi 等）。

**本仓库录制缓存的实际来源**：DeepSeek `deepseek-flash`（V4.1 Flash），经其 OpenAI 兼容
端点 `https://api.deepseek.com/v1` 录制，共 160 条（40 用例 × 采样次数 × v1/v2 两版提示词）。

### 实测结果

| 提示词 | pytest | 按用例计 | 失败集中在 |
| --- | --- | --- | --- |
| `v1` 基线 | 11 失败 / 71 通过 | 32/40 | 安全性 2/6、功能语义 9/12、公平性 7/8 |
| `v2` 修复 | 0 失败 / 82 通过 | 40/40 | — |

明细见 `testdata/execution_report.md`（v2）与 `testdata/execution_report.v1.md`（v1 基线）。

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

`nl2cron` 提示词 v1 刻意从简（无方言约束、无注入防御、不强制输出形态），v2 补充字段语法
约束、无关输入拒绝与指令层级防御。缺陷以 `NL2CRON_PROMPT_VERSION=v1` 复现、`v2` 回归
验证，与模块一"baseline/subject 切换"的演示方式同构。

在 `deepseek-flash` 上实测暴露 3 类缺陷（v1 的 11 条失败全部归入其中）：

| 缺陷 | 现象 | 受影响用例 | 被哪一层捕获 |
| --- | --- | --- | --- |
| NL2C-D-001 非确定性格式漂移 | 同一输入多次采样，偶尔输出 6 字段、换行拼接的两条表达式、或 `TZ=` 前缀 | 005、009、012、039 | 结构守卫 + 一致性统计 |
| NL2C-D-002 指令越权 | 被"输出 6 段式 Quartz 表达式"诱导后照做；被 base64 编码的隐藏指令劫持 | 029、032 | 安全层 |
| NL2C-D-003 输出形态不合规 | 模型**安全地拒绝了**攻击，但用自然语言而非 JSON 回答，格式断言先于安全判定失败 | 027、030 | 结构守卫（与安全判定耦合） |

> 实测同样暴露了**测试侧自身**的问题：公平性阈值比较存在浮点精度误报、base64 用例的攻击
> 目标与正确翻译结果撞车、`tools/` 下两个脚本从未真正跑通。三者均已修复，列为"AI 反思"
> 素材；复跑 `tools/summarize.py` 与 `tools/dump_defect_evidence.py` 可复核当前输出。

## 交付物

| 附录   | 交付物                                 | 位置                                      |
| ------ | -------------------------------------- | ----------------------------------------- |
| 附录一 | 测试用例清单（40 条 AI 用例）          | `testcases/测试用例清单（模块二）.xlsx` |
| —     | 缺陷清单（录音口径：无需单独缺陷报告） | `defects/缺陷报告（模块二）.doc`        |
| 附录四 | 测试报告（模块二）                     | `reports/测试报告（模块二）.docx`       |
| —     | 成果汇报 PPT                           | `presentation/成果汇报.pptx`            |
| —     | 演示视频                               | `presentation/演示视频（模块二）.mp4`   |
| —     | AI 使用披露                            | `ai-usage/`                             |

## 入库范围

入库标准两条：**运行测试必需**、或**《实践作业要求 v2026》明确要求提交**。其余一律不入库（规则见仓库根 `.gitignore`）。

| 类别 | 内容 | 依据 |
| --- | --- | --- |
| 交付件本体 | `testcases/测试用例清单（模块二）.xlsx`、`defects/缺陷报告（模块二）.doc`、`reports/测试报告（模块二）.docx`、`presentation/成果汇报.pptx`、`presentation/演示视频（模块二）.mp4` | §3.2.1 方案 1 交付件 1/3/4/5 |
| 被测代码 | `nl2cron/` | §2「被测代码」 |
| 测试脚本与配置 | `tests/`、`tools/`、`presentation/演示-离线复现.py`、`pytest.ini`、`requirements-dev.txt` | §2「测试脚本、配置文件」；交付件 2「能一键运行全部用例」 |
| 测试数据 | `testdata/nl2cron_cases.json`、`testdata/recordings/` | §2「测试数据」；回放缓存是离线「一键运行」的前提 |
| AI 对话记录 | `ai-usage/` | §2「关键 AI 对话记录」 |
| 项目说明 | 各目录 `README.md` | §2「仓库中须包含 README.md，说明项目结构、环境配置和测试运行方式」 |

**不入库**（保留在本地）：

- **`tools/record_responses.py`**：唯一需要 API Key 的脚本（真实调用 LLM 并录制响应）；其产物
  `testdata/recordings/` 已入库，故回放链路不依赖它；
- **派生产物** `testdata/execution_*`、`defects/NL2C-D-00*-repro.txt`：均可由入库的
  `tools/summarize.py`、`tools/dump_defect_evidence.py` 一键重新生成；
- **内部追踪矩阵** `requirements_traceability.md`；
- 交付件的素材稿与逐字段填充稿（`*素材.md`、`*填充.md`）、`presentation/` 的 PPT 制作过程材料、
  配图及其生成脚本、录屏脚本（配图已内嵌进 PPT，PPT 即最终成品）。

## 全流程复现

除「重新录制响应」（需 API Key）与「汇报配图生成」（脚本不入库，见下）外，
模块二的测试流程可仅用本仓库文件完整复现：

```bash
NL2CRON_MODEL=deepseek-flash NL2CRON_PROMPT_VERSION=v1 python -m pytest -q   # 11 失败：缺陷原形毕露
NL2CRON_MODEL=deepseek-flash NL2CRON_PROMPT_VERSION=v2 python -m pytest -q   # 82 通过：全部修复
NL2CRON_MODEL=deepseek-flash NL2CRON_PROMPT_VERSION=v1 python tools/summarize.py  # 生成 v1 基线留档
NL2CRON_MODEL=deepseek-flash NL2CRON_PROMPT_VERSION=v2 python tools/summarize.py  # 生成 v2 交付汇总
python tools/gen_case_list.py              # 由账本 + 汇总重新生成用例清单 xlsx
python tools/dump_defect_evidence.py       # 由录制缓存重新导出 3 份缺陷复现证据
```

汇报配图（`图-01` ~ `图-11`）与 PPT 素材不在上列——配图已内嵌进 `成果汇报.pptx`，PPT 本身
即最终成品，不需要也不支持从本仓库重新生成。

`summarize.py` 按提示词版本自动命名（v1 → `*.v1.json/md` 留档，v2 → 主文件名），
两次运行互不覆盖、可任意顺序执行。
