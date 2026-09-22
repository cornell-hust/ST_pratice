# 模块二需求追踪矩阵

本文把课程要求（《实践作业要求v2026.pdf》方案 1 及课程录音中的教师口径）与测试用例、
自动化实现和缺陷证据关联起来。与模块一的追踪矩阵同一用途：报告中的数字都从这里取。

## 需求到证据映射

| 需求 ID | 课程要求/验收点 | 用例范围 | 自动化实现 | 交付证据 |
|---|---|---|---|---|
| M2-R01 | 被测对象含 AI 模型（方案 1），在模块一系统上添加 LLM 组件 | 全部用例 | `nl2cron/`（translate 入口、提示词 v1/v2、守卫） | `module2/nl2cron/README.md` |
| M2-R02 | AI 相关测试用例 ≥15 条 | 账本 36 条（functional 12 / robustness 10 / directional 4 / safety 6 / fairness 8） | `tests/test_*.py` 按 `testdata/nl2cron_cases.json` 参数化 | `testcases/测试用例清单（模块二）.xlsx` |
| M2-R03 | 覆盖鲁棒性/公平性/安全性 | INV 10 条、FAIR 4 组 8 条、SAF 6 条 | `test_robustness.py` / `test_fairness.py` / `test_safety.py` | `testdata/execution_report.md` |
| M2-R04 | 自动化脚本一键运行全部用例，附 README | 全部 36 条 | `python -m pytest -q`（回放模式离线确定性运行） | `module2/README.md` |
| M2-R05 | 有效缺陷 ≥1（现象/复现/修复验证） | 目标 3 个：`NL2C-D-001` 起 | 失败用例即回归用例；`NL2CRON_PROMPT_VERSION=v1` 复现 / `v2` 验证修复 | `defects/缺陷清单（模块二）.docx`、`defects/NL2C-D-00X-repro.txt` |
| M2-R06 | 测试报告按附录四，含 AI 反思 | — | — | `reports/测试报告（模块二）.docx` |
| M2-R07 | 成果汇报 PPT + 演示视频 | — | `presentation/演示-离线复现.py`（现场无网络兜底） | `presentation/` |
| M2-R08 | Git 版本管理，成员独立提交，AI 使用披露 | — | 两成员各自 commit；提示词 v1/v2 演进留痕 | `ai-usage/`、Git 历史 |

## 用例到实现登记表

| 用例编号范围 | 测试主题 | 测试文件/函数 | 方法 | 状态 |
|---|---|---|---|---|
| 待账本定稿后回填 | 功能语义（CheckList MFT） | `tests/test_functional.py::test_mft_reference` | 等价类、边界值、场景法 | 待执行 |
| 待回填 | 方向性蜕变（DIR） | `tests/test_functional.py::test_dir_reference` | 蜕变测试 | 待执行 |
| 待回填 | 鲁棒性（INV） | `tests/test_robustness.py::test_inv` | 错误推测、语法校验 | 待执行 |
| 待回填 | 安全性（SAF） | `tests/test_safety.py::test_safe` | 安全测试（OWASP LLM Top 10 映射） | 待执行 |
| 待回填 | 公平性（FAIR，4 组对照） | `tests/test_fairness.py::test_fair_group` | 对照实验 | 待执行 |
| 待回填 | 非确定性一致性 | `tests/test_consistency.py::test_run_agreement` | 多次采样统计 | 待执行 |

## 缺陷到回归证据

| 缺陷 ID | 现象 | 基线复现（v1 提示词） | 修复 | 验证用例 | 状态 |
|---|---|---|---|---|---|
| 待 D1 分诊后回填 | | | | | |

## 执行记录

| 项目 | 结果 |
|---|---|
| 总用例数 | 36（账本定稿后核对） |
| 通过/失败 | 待执行后回填（`testdata/execution_report.md`） |
| 缺陷 | 待 D1 分诊后回填 |
| 最近执行命令 | `NL2CRON_PROMPT_VERSION=v1 python tools/summarize.py`（基线）；`NL2CRON_PROMPT_VERSION=v2 python tools/summarize.py`（修复后） |

任何"通过/已修复"结论都必须能由回放缓存 + 测试输出追溯：任何人克隆仓库后执行
`python -m pytest -q` 即可离线复现同一结果，无需 API Key。
