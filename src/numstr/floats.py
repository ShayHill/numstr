"""Represent numbers as limited-precision floats without extra characters.

To reduce file size and increase readibility.

These numbers are appropriate for SVG and other formats where
* maximum precision is not necessary or even supported
* -0 is equivalent to 0
* 1 is equivalent to 1.0
* scientific notation is not supported

:author: Shay Hill
:created: 2024-03-23
"""

from __future__ import annotations

import functools as ft
import operator as op
import re
from typing import TYPE_CHECKING, SupportsFloat

if TYPE_CHECKING:
    from collections.abc import Callable


_RE_FLOAT = re.compile(r"[-+]?\d*\.?\d+([eE][-+]?\d+)?")

_MAX_SIGNED_INT = 2**31 - 1

NDIGITS = 6


def format_number(num: SupportsFloat | float | str, ndigits: None | int = None) -> str:
    """Format strings at limited precision. Remove extra characters.

    :param num: anything that can print as a float.
    :param ndigits: number of digits to keep after the decimal point (default 6).
        <1 is the same as 0.
    :return: str

    * reduce fp precision to ndigits
    * remove trailing zeros
    * remove trailing decimal point (floats == int(num) will be printed as ints)
    * convert "-0" to "0"
    * return _MAX_SIGNED_INT if num > _MAX_SIGNED_INT
    * return -_MAX_SIGNED_INT if num < -_MAX_SIGNED_INT
    """
    as_float = float(num)
    if as_float > _MAX_SIGNED_INT:
        return str(_MAX_SIGNED_INT)
    if as_float < -_MAX_SIGNED_INT:
        return str(-_MAX_SIGNED_INT)

    ndigits = ndigits if ndigits is not None else NDIGITS
    if ndigits >= 0:
        fstr = f"{{:.{ndigits}f}}"
    else:
        fstr = "{:f}"

    as_str = fstr.format(as_float).rstrip("0").rstrip(".")
    if as_str == "-0":
        return "0"
    return as_str


def format_numbers(
    *nums: SupportsFloat | float | str, ndigits: None | int = None
) -> map[str]:
    """Format multiple strings to limited precision.

    :param nums: iterable of floats
    :return: list of formatted strings
    """
    format_to_ndigits = ft.partial(format_number, ndigits=ndigits)
    return map(format_to_ndigits, nums)


def extract_float_strs(data: str) -> tuple[str, map[str]]:
    """Extract float substrings from a string.

    :param data: string with floats
    :return: template, float substrings
    """
    template = data.replace("{", "{{").replace("}", "}}")
    template = _RE_FLOAT.sub("{}", template)
    return template, map(op.methodcaller("group"), _RE_FLOAT.finditer(data))


def extract_floats(data: str) -> tuple[str, map[float]]:
    """Extract floats from a string.

    :param data: string with floats
    :return: template, floats
    """
    template, float_strs = extract_float_strs(data)
    return template, map(float, float_strs)


def map_floats(func: Callable[[float], str], data: str) -> str:
    """Map a function to floats in a string.

    :param func: function to apply to floats
    :param data: string with floats
    :return: string with each float replaced by func(float)
    """
    template, floats = extract_floats(data)
    return template.format(*map(func, floats))


def format_numbers_in_string(data: str, ndigits: None | int = None) -> str:
    """Find and format floats in a string.

    :param data: string with floats or a float value
    :return: string with floats formatted to limited precision

    Works as a more robust version of format_number. Will correctly handle input
    floats in exponential notation, but will experience silent with strings like
    "a0b1c2d3e4", because "3e4" will be recognized and treated as exponential
    notation. Nothing I use this for, certainly not SVGs, will have strings like that
    in the specification, but you might put one in a value of a text attribute. It is
    not safe to format text attribute values with this function.
    """
    format_to_ndigits = ft.partial(format_number, ndigits=ndigits)
    return map_floats(format_to_ndigits, str(data))
