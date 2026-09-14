# -*- coding: utf-8 -*-
"""模块一演示视频 · 缺陷复现脚本（同一段代码，跑两遍）

运行方式（在 module1 目录下，Git Bash）——
第 1 遍（缺陷版本 baseline 6.2.2 原版）：
    PYTHONPATH=baseline .venv/Scripts/python.exe presentation/演示-缺陷复现.py
第 2 遍（修复后 subject）：
    PYTHONPATH=subject  .venv/Scripts/python.exe presentation/演示-缺陷复现.py

PowerShell 写法：
    $env:PYTHONPATH="baseline"; .venv/Scripts/python.exe presentation/演示-缺陷复现.py

脚本先打印实际加载的 croniter 路径，用于证明两遍运行加载的确实不是同一份源码。
"""
import sys
from datetime import datetime

# Git Bash / mintty 下 stdout 是管道：强制 UTF-8 + 行缓冲，避免中文乱码
sys.stdout.reconfigure(encoding="utf-8", errors="replace", line_buffering=True)

import croniter as pkg
from croniter import croniter

print("实际加载的源码：", pkg.__file__)
print("=" * 64)

print("缺陷 1：零步长范围  表达式 0 0 * * 5-5/0")
try:
    croniter("0 0 * * 5-5/0", datetime(2024, 1, 1))
    print("  未抛异常")
except Exception as exc:
    print(f"  {type(exc).__name__}: {exc}")

print("\n缺陷 2：月份低界偏移  表达式 0 0 1 */2 *  起点 2024-02-01（expand_from_start_time=True）")
try:
    print("  下一次:", croniter("0 0 1 */2 *", datetime(2024, 2, 1),
                               expand_from_start_time=True).get_next(datetime))
except Exception as exc:
    print(f"  {type(exc).__name__}: {exc}")

print("\n缺陷 3：Sunday 相位错位  表达式 0 0 * * 1-7/2  起点 2024-01-07（周日）")
it = croniter("0 0 * * 1-7/2", datetime(2024, 1, 7), expand_from_start_time=True)
print("  连续 4 次:", [it.get_next(datetime).strftime("%Y-%m-%d") for _ in range(4)])
print("  正确相位应为 01-09、01-11、01-13、01-14（隔天，且不落在周日 01-07）")
