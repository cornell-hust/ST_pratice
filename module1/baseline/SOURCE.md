# 基线源码（croniter 6.2.2 修复前）

本目录保存 **未应用任何历史缺陷修复** 的 croniter 6.2.2 源码，用于手动复现三个历史缺陷（CRON-D-001 ~ CRON-D-003）的基线行为。

- 来源：仓库 git 提交 `7deb785`（feat(module1): 固定 croniter 6.2.2 被测源码快照）
- 上游：https://github.com/pallets-eco/croniter 的 6.2.2 版本
- 与 `module1/subject/` 的差异：`subject/` 为应用了三个缺陷修复后的源码；本目录为修复前的原始快照

## 用法

在 `module1` 目录下，用 `PYTHONPATH` 指向本目录即可加载基线版本（与修复后版本对比测试）：

```bash
# Git Bash
PYTHONPATH=baseline .venv/Scripts/python.exe        # 基线（有 bug）
PYTHONPATH=subject  .venv/Scripts/python.exe        # 修复后

# PowerShell
$env:PYTHONPATH="baseline"; .venv\Scripts\python.exe
$env:PYTHONPATH="subject";  .venv\Scripts\python.exe
```

注意：`PYTHONPATH` 会保留在当前终端会话中，切换环境时需重新设置或清除（Git Bash：`unset PYTHONPATH`；PowerShell：`Remove-Item Env:PYTHONPATH`）。

## 三个缺陷的基线复现命令

```python
from croniter import croniter
from datetime import datetime

# CRON-D-001（issue #232）：零步长 → 裸 ValueError
croniter('0 0 * * 5-5/0', datetime(2024, 1, 1))

# CRON-D-002（issue #235）：每两个月 1 号，从 2 月出发 → 报错 out of range
croniter('0 0 1 */2 *', datetime(2024, 2, 1), expand_from_start_time=True).get_next(datetime)

# CRON-D-003（issue #239）：隔天步进，从周日出发 → 序列错位一天（01-08 起）
it = croniter('0 0 * * 1-7/2', datetime(2024, 1, 7), expand_from_start_time=True)
[it.get_next(datetime) for _ in range(4)]
```

基线实际输出以 `module1/defects/repro-baseline.txt` 记录为准。
