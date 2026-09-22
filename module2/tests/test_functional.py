"""功能语义（MFT）与方向性蜕变（DIR）用例。"""

import pytest

from checks import check_reference
from ledger import ids, of_dimension

FUNCTIONAL_CASES = of_dimension("functional")
DIRECTIONAL_CASES = of_dimension("directional")


@pytest.mark.functional
@pytest.mark.parametrize("case", FUNCTIONAL_CASES, ids=ids(FUNCTIONAL_CASES))
def test_mft_reference(case):
    check_reference(case)


@pytest.mark.directional
@pytest.mark.parametrize("case", DIRECTIONAL_CASES, ids=ids(DIRECTIONAL_CASES))
def test_dir_reference(case):
    check_reference(case)
