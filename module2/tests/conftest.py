"""pytest 全局配置：把 module2 根目录与 module1/subject 快照注入 sys.path。

module1/subject 提供守卫与 oracle 依赖的 croniter；module2 根目录提供 nl2cron 包。
"""

import sys
from pathlib import Path

MODULE2_ROOT = Path(__file__).resolve().parents[1]
MODULE1_SUBJECT = MODULE2_ROOT.parent / "module1" / "subject"

for path in (str(MODULE1_SUBJECT), str(MODULE2_ROOT)):
    if path not in sys.path:
        sys.path.insert(0, path)
