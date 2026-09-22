"""鲁棒性（INV）用例：同义改写须语义不变；无意义输入须体面处理。"""

import pytest

from checks import check_graceful, check_reference
from ledger import ids, of_dimension

ROBUST_CASES = of_dimension("robustness")


@pytest.mark.robustness
@pytest.mark.parametrize("case", ROBUST_CASES, ids=ids(ROBUST_CASES))
def test_inv(case):
    if case["expect"] == "reference":
        check_reference(case)
    else:
        check_graceful(case)
