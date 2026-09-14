# defects/ — 缺陷报告与证据（附录二）

| 文件 | 作用 |
| --- | --- |
| `缺陷报告.doc` | **课程附录二交付文件**：CRON-D-001—003 的缺陷现象、复现步骤、修复验证 |
| `croniter-history.md` | 三个历史缺陷的汇总：上游依据、复现、根因、修复 |
| `repro-baseline.txt` | 修复前基线（6.2.2 原版）的复现输出 |
| `repro-fixed.txt` | 修复后的复核输出 |

## 缺陷与回归用例对应关系

| 缺陷编号 | 上游依据 | 基线表现 | 回归用例 |
| --- | --- | --- | --- |
| CRON-D-001 | issue #232 | 抛 Python 裸异常 `ValueError`，而非标准 `CroniterBadCronError` | CRON-UT-033 |
| CRON-D-002 | issue #235 | 合法表达式 `0 0 1 */2 *` 报"超出范围"，算不出触发时间 | CRON-UT-034 |
| CRON-D-003 | issue #239 | 隔天序列相位错位一天，**不报错、静默返回错误结果** | CRON-UT-035 |

完整映射见 `module1/requirements_traceability.md`。

## 复现方式

在 `module1` 目录下执行（Git Bash）：

```bash
PYTHONPATH=baseline .venv/Scripts/python.exe presentation/演示-缺陷复现.py   # 6.2.2 原版：三个缺陷原形毕露
PYTHONPATH=subject  .venv/Scripts/python.exe presentation/演示-缺陷复现.py   # 修复后：三个缺陷全部消失
```

## 新增缺陷证据的存放约定

- 证据文件（复现输出、日志）放本目录，文件名以缺陷编号开头，如 `CRON-D-004-repro.txt`；
- **没有复现输出的缺陷不得标记为"已关闭"**；
- 缺陷的认定依据应为上游 issue／CHANGELOG 加本地可复现的运行输出，不以推测代替证据。
