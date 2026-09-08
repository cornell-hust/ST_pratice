# croniter 6.2.2 历史缺陷证据

基线：官方 `croniter` 6.2.2（`module1/subject/SOURCE.md`）。复现环境：Python 3，`PYTHONPATH=module1/subject`。

## CRON-D-001 零步长范围未稳定拒绝

- 来源：CHANGELOG 6.2.3，issue #232；https://github.com/pallets-eco/croniter/blob/main/CHANGELOG.rst
- 步骤：执行 `croniter("0 0 * * 5-5/0", datetime(2024,1,1))`。
- 基线实际：抛出裸 `ValueError: range() arg 3 must not be zero`，不属于 `CroniterError`。
- 期望：抛出稳定的 `CroniterBadCronError`。
- 根因：范围展开前未校验 `step == 0`。
- 修复：在 `croniter.py` 将零步长转换为 `CroniterBadCronError`。
- 修复后：同命令抛出 `CroniterBadCronError`；合法 `*/5` 保持通过。
- 修复 commit：见 Git 历史。

## CRON-D-002 expand_from_start_time 月份低边界偏移

- 来源：CHANGELOG 6.2.3，issue #235；https://github.com/pallets-eco/croniter/blob/main/CHANGELOG.rst
- 步骤：从 `2024-02-01` 对 `0 0 1 */2 *` 调用 `get_next(datetime)`。
- 基线实际：直接报 `CroniterBadCronError ... out of range`（月份余数为 0 被当作下界）。
- 期望：按两个月周期返回 `2024-04-01`、`2024-06-01`……。
- 根因：月份低界计算使用 `dt.month % step`，余数为 0 时得到非法月份 0。
- 修复：余数为 0 时使用步长作为低界。
- 修复后：返回 `2024-04-01`、`2024-06-01`、`2024-08-01`……。
- 修复 commit：见 Git 历史。

## CRON-D-003 Sunday 步进低边界错误

- 来源：CHANGELOG 6.2.4，issue #239；https://github.com/pallets-eco/croniter/blob/main/CHANGELOG.rst
- 步骤：从 Sunday `2024-01-07` 对 `0 0 * * 1-7/2` 启用 `expand_from_start_time`。
- 基线实际：返回 `2024-01-08`、`2024-01-10`、`2024-01-12`，Sunday 相位被错误计算。
- 期望：以 cron 的 Sunday=0 语义计算步进边界。
- 根因：使用 `weekday()+1`，将 Sunday 映射为 7 而非 0。
- 修复：改用 `isoweekday() % 7`。
- 修复后：相位序列为 `2024-01-09`、`2024-01-11`、`2024-01-13`、`2024-01-14`……。
- 修复 commit：见 Git 历史。

完整基线输出保存在 `repro-baseline.txt`；修复后结果由针对性命令复核。
