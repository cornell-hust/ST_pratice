# testdata/ — 测试数据账本

`cron_cases.json` 是 36 条清单用例（CRON-UT-001—036）的**单一数据源**：用例的表达式、起始时间与预期结果全部记录在此，测试代码不写死任何用例数据（"数据带着代码"，设计动机见 `module1/自动化测试设计与实施说明v2.md`）。

## 字段说明

| 字段 | 含义 | 出现条件 |
|---|---|---|
| `id` | 用例编号 `CRON-UT-XXX` | 全部 |
| `category` | `equivalence` / `boundary` / `scenario` / `regression` | 全部 |
| `expr` | cron 表达式 | 全部 |
| `valid` | `true`=合法表达式应通过；`false`=应抛 `CroniterBadCronError` | equivalence |
| `start` | 起始时间（ISO 8601） | boundary / scenario / regression |
| `expected` | 单次 `get_next` 的预期时间 | boundary |
| `expect` | `"raise"` 或 `"sequence"` | regression |
| `n` | 取前 n 次结果 | sequence 类 |
| `expected`（数组） | 完整预期序列 | sequence 类 |

## 修改规则

- 改用例 = 改本文件，测试代码不动；
- 编号连续、不重号；新数据先在此登记，再跑全量 pytest 验证；
- 附录一清单与本文件保持一一对应，修改后同步回填清单并更新 `requirements_traceability.md`。
