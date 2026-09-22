"""croniter 依赖注入：复用模块一被测库 croniter 的仓库内快照（module1/subject）。

输出守卫与 oracle 都要用 croniter；直接指向仓库内快照保证离线可复现、版本固定，
同时体现模块二对模块一资产的延续使用。
"""

import sys
from pathlib import Path

_SUBJECT = Path(__file__).resolve().parents[2] / "module1" / "subject"
if _SUBJECT.is_dir() and str(_SUBJECT) not in sys.path:
    sys.path.insert(0, str(_SUBJECT))
