# 模块一需求追踪矩阵

本文把课程要求（来源为《实践作业要求v2026.pdf》及《课程录音总结.md》）与测试用例、自动化实现和缺陷证据关联起来。附录文件中的要求属于课程交付约束；本项目文档仅记录执行方式，不改变课程原文。

## 需求到证据映射

| 需求 ID | 课程要求/验收点 | 用例范围 | 自动化实现 | 缺陷/交付证据 |
|---|---|---|---|---|
| M1-R01 | 被测对象、版本和来源可复现 | CRON-UT-001—CRON-UT-004 | `tests/conftest.py`、`tests/test_croniter.py` | `subject/croniter/SOURCE.md` |
| M1-R02 | 用例不少于 30 条，采用等价类、边界值、场景法等方法 | CRON-UT-001—025、033—036，去重后共 29 条（低于 30 条要求，需补充） | `testdata/cron_cases.json`、`tests/test_croniter.py` | `testcases/` 附录一 |
| M1-R03 | 覆盖表达式解析、迭代、匹配、范围和时区 | CRON-UT-005—CRON-UT-025 | `tests/test_croniter.py` | 34 条测试通过 |
| M1-R04 | 自动化比例达到课程要求（计划至少 80%） | 29 条清单用例全部自动化，另有5条专项检查 | `python -m pytest -q` | 当前测试集：34 passed |
| M1-R05 | 至少三个真实历史缺陷，完成复现、修复和回归 | CRON-UT-033—CRON-UT-036 | `-m regression` 标记的回归测试 | `CRON-D-001`—`CRON-D-003`；修复提交 `07dfad8`、`101f39e`、`10e9bb6` |
| M1-R06 | 测试报告按附录三提交并披露 AI 使用 | 典型用例 CRON-UT-013、014、015、033、034、035 | 覆盖率和执行摘要 | `reports/附录3-测试报告-模块一.docx` |

## 用例到实现登记表

实现测试时，每个测试函数至少登记一个连续的用例编号；同一函数可通过参数化承载多个用例。下表先固定接口位置，执行后补充函数名、结果和日期。

| 用例编号范围 | 测试主题 | 测试文件/函数 | 方法 | 状态 |
|---|---|---|---|---|
| CRON-UT-001—012 | 合法/非法表达式与字段等价类 | `tests/test_croniter.py::test_parser_equivalence` | 等价类、异常 | 已通过 |
| CRON-UT-013—024 | 分钟、小时、日期、月份、闰年和月末边界 | `tests/test_croniter.py::test_next_boundaries` | 边界值 | 已通过 |
| CRON-UT-025（原 025—032 为 8 条输入完全相同的重复用例，已去重保留 1 条） | 连续迭代、范围枚举、匹配和时区场景 | `tests/test_croniter.py::test_scenarios`、`test_match_and_range` | 场景法、状态转换 | 已通过 |
| CRON-UT-033—036 | 三个历史缺陷及修复后回归 | `tests/test_croniter.py::test_regressions` | 回归、异常 | 已通过 |

## 缺陷到回归证据

| 缺陷 ID | 上游依据 | 基线复现 | 修复位置/提交 | 回归用例 | 状态 |
|---|---|---|---|---|---|
| CRON-D-001 | croniter 6.2.3 CHANGELOG / issue #232 | 已复现并回归 | `07dfad8` | CRON-UT-033 | 已修复 |
| CRON-D-002 | croniter 6.2.3 CHANGELOG / issue #235 | 已复现并回归 | 源码修复 `07dfad8`；证据修订 `10e9bb6` | CRON-UT-034 | 已修复 |
| CRON-D-003 | croniter 6.2.4 CHANGELOG / issue #239 | 已复现并回归 | 源码修复 `07dfad8`；证据提交 `101f39e` | CRON-UT-035 | 已修复 |

## 执行记录

| 项目 | 结果 |
|---|---|
| 总用例数 | 29 条清单用例 + 5 条专项自动化检查 = 34（CRON-UT-026—032 重复用例已去重） |
| 自动化用例数/比例 | 34 条 pytest 用例通过 |
| 通过/失败/跳过 | 34 / 0 / 0 |
| 语句覆盖率/分支覆盖率 | branch coverage 56%（当前测试集，未达到原计划 85% 目标） |
| 缺陷复现与回归 | 3 个历史缺陷均已复现、修复并通过回归；修复提交 `07dfad8`、`101f39e`、`10e9bb6` |
| 最近一次执行命令和日期 | `.venv/Scripts/python.exe -m pytest -q -c pytest.ini`（module1 目录内）；2026-09-10 |

任何“通过”“已修复”或覆盖率数字都必须能由测试输出、报告附件或 Git diff 追溯；成员姓名和贡献比例提交前仍需由小组填写并核对总和为100%。
