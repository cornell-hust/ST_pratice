# testdata/ — 测试数据账本

`cron_cases.json` 是 43 条清单用例（CRON-UT-001—011、013—025、033—035、037—052；012 已删除、026—032 重复用例已去重、036 已删除，原 5 条专项检查并入为 041—050，另新增 051—052 夏令时用例）的**单一数据源**：用例的表达式、起始时间与预期结果全部记录在此，测试代码不写死任何用例数据（"数据带着代码"，设计动机见 `module1/自动化测试设计与实施说明v2.md`）。

## 字段说明

| 字段 | 含义 | 出现条件 |
|---|---|---|
| `id` | 用例编号 `CRON-UT-XXX` | 全部 |
| `category` | `equivalence` / `boundary` / `scenario`（设计方法，共三类） | 全部 |
| `expr` | cron 表达式 | 全部 |
| `valid` | `true`=合法表达式应通过；`false`=应抛 `CroniterBadCronError` | equivalence |
| `start` | 起始时间（ISO 8601）；`"object"` 表示非法起始类型（应抛 TypeError/ValueError） | boundary / scenario / equivalence（is_valid 类无 start） |
| `expected` | 单次 `get_next` 的预期时间；045—049 为布尔判定结果 | boundary / equivalence |
| `expand` | `true` 时按起点展开步进（`expand_from_start_time=True`），用于在基线版本上暴露月份/周日低界缺陷 | boundary（当前仅 034/035 使用） |
| `ret_type` | `"float"`：断言默认返回类型为秒级时间戳 | boundary（仅 042 使用） |
| `tz` | ZoneInfo 时区名（如 `America/New_York`），覆盖 start 的固定偏移 | boundary（043 普通日、051 春季跳变日、052 秋季回拨日） |
| `check` | `match` / `match_range` / `range` / `is_valid`：功能校验类型（设计方法仍由 category 表达） | equivalence（045—049）/ scenario（050） |
| `end` | 时段/窗口结束时间（ISO 8601） | equivalence（047/048）/ scenario（050） |
| `count` | 窗口内触发点个数 | scenario（050） |
| `second_at_beginning` | `true` 时 is_valid 按秒在前解析 6 段表达式 | equivalence（is_valid，仅 049 使用） |

## 修改规则

- 改用例 = 改本文件，测试代码不动；
- 编号连续、不重号；新数据先在此登记，再跑全量 pytest 验证；
- 附录一清单与本文件保持一一对应，修改后同步回填清单并更新 `requirements_traceability.md`。
