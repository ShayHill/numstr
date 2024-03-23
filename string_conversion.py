"""Quasi-private functions for high-level string conversion.

:author: Shay Hill
:created: 7/26/2020

Rounding some numbers to ensure quality svg rendering:
* Rounding floats to six digits after the decimal
* Rounding viewBox dimensions to ints
"""

from __future__ import annotations

import re
from contextlib import suppress
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from collections.abc import Iterable


def format_number(num: float | str) -> str:
    """Format strings at limited precision.

    :param num: anything that can print as a float.
    :return: str

    I've read articles that recommend no more than four digits before and two digits
    after the decimal point to ensure good svg rendering. I'm being generous and
    giving six. Mostly to eliminate exponential notation, but I'm "rstripping" the
    strings to reduce filesize and increase readability

    * reduce fp precision to 6 digits
    * remove trailing zeros
    * remove trailing decimal point
    * convert "-0" to "0"
    """
    as_str = f"{float(num):0.6f}".rstrip("0").rstrip(".")
    if as_str == "-0":
        as_str = "0"
    return as_str


def format_numbers(
    nums: Iterable[float] | Iterable[str] | Iterable[float | str],
) -> list[str]:
    """Format multiple strings to limited precision.

    :param nums: iterable of floats
    :return: list of formatted strings
    """
    return [format_number(num) for num in nums]


def _is_float_or_float_str(data: float | str) -> bool:
    """Check if a string is a float.

    :param data: string to check
    :return: bool
    """
    try:
        _ = float(data)
    except ValueError:
        return False
    else:
        return True


def format_numbers_in_string(data: float | str) -> str:
    """Find and format floats in a string.

    :param data: string with floats or a float value
    :return: string with floats formatted to limited precision

    Works as a more robust version of format_number. Will correctly handle input
    floats in exponential notation. This should work for and parameter value in an
    svg except 'text'. The function will fail with input strings like
    'ice3.14bucket', because 'e3.14' will be identified as a float. SVG param values
    will not have such strings, but the 'text' attribute could. This function will
    not handle that case. Do not attempt to reformat 'text' attribute values.
    """
    with suppress(ValueError):
        # try as a regular number to strip spaces from simple float strings
        return format_number(data)
    words = re.split(r"([^\d.eE-]+)", str(data))
    words = [format_number(w) if _is_float_or_float_str(w) else w for w in words]
    return "".join(words)
