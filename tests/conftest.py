"""See full diffs in pytest.

:author: Shay Hill
:created: 2023-10-07
"""

from typing import Any
import pytest
from pathlib import Path


def pytest_assertrepr_compare(config: Any, op: str, left: str, right: str):
    """See full error diffs"""
    if op in ("==", "!="):
        return ["{0} {1} {2}".format(left, op, right)]


_RESOURCES = Path(__file__, "..", "resources")


def _read_romans() -> list[str]:
    """Read the roman-numeral resource file."""
    with (_RESOURCES / "roman_1_to_3999").open() as f:
        romans = [x.strip() for x in f.readlines() if x.strip()]
    return [x for x in romans if x]


_ROMANS_1_TO_3999 = _read_romans()


@pytest.fixture(scope="function", params=enumerate(_ROMANS_1_TO_3999, start=1))
def roman_1_to_3999(request: Any) -> tuple[int, str]:
    """Yield lowercase Roman numeral strings from 1 to 3999."""
    return request.param


@pytest.fixture(scope="function", params=range(1, 4001))
def positive_ints(request: Any) -> int:
    """Yield positive numbers from 1 to 4000."""
    return request.param
