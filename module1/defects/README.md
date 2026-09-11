# defects/ — 缺陷报告与证据（附录二）

| 文件 | 作用 |
|---|---|
| `附录2-缺陷报告.docx` | 课程附录二交付文件 |
| `croniter-history.md` | CRON-D-001—003 三个历史缺陷的汇总（依据、复现、根因、修复） |
| `repro-baseline.txt` | 修复前基线（6.2.2）的复现输出 |
| `repro-fixed.txt` | 修复后的复核输出 |

缺陷与回归用例对应关系：CRON-D-001→CRON-UT-033，CRON-D-002→CRON-UT-034，CRON-D-003→CRON-UT-035（详见 `requirements_traceability.md`）。

> 归属说明：原 `module1/bug1.md`、`bug2.md`、`bug3.md`（三个缺陷的通俗讲解）已于 2026-09-11 清理——其内容与本目录的 `croniter-history.md`、`附录2-缺陷报告.docx` 重复；备份见仓库外的 `ST_pratice_已删除文件备份_20260911.zip`。

新增缺陷证据的存放约定：证据文件（复现输出、日志）放本目录，文件名以缺陷编号开头（如 `CRON-D-004-repro.txt`）；没有复现输出的缺陷不得标记为"已关闭"。
