"""安全性（SAF）用例：提示注入 / 提示词泄露 / 输出劫持（OWASP LLM01/LLM05 映射）。"""

import pytest

from checks import check_safe
from ledger import ids, of_dimension

SAFETY_CASES = of_dimension("safety")


@pytest.mark.safety
@pytest.mark.parametrize("case", SAFETY_CASES, ids=ids(SAFETY_CASES))
def test_safe(case):
    check_safe(case)
