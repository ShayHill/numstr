"""Test functions in string_conversion.py.

:author: Shay Hill
:created: 2023-09-23
"""

import numstr as mod


class TestFormatNuber:
    def test_negative_zero(self):
        """Remove "-" from "-0"."""
        assert mod.format_number(-0.0000000001) == "0"

    def test_round_to_int(self):
        """Round to int if no decimal values !- 0."""
        assert mod.format_number(1.0000000001) == "1"

    def test_exponential_notation(self):
        """Return exponential notation."""
        assert mod.format_number("3.14159e-10") == "0"

    def test_exponential_notation_big_e(self):
        """Return exponential notation."""
        assert mod.format_number("3.14159E-10") == "0"

    def test_non_default_precision(self):
        """Return exponential notation."""
        assert mod.format_number("3.14159", 3) == "3.142"

    def test_zero_precision(self):
        """Return exponential notation."""
        assert mod.format_number("3.9", 0) == "4"

    def test_negative_precision(self):
        """Return the number as a string."""
        assert mod.format_number(3.14159, -1) == "3.14159"

    def test_infinity(self):
        """Return max int."""
        assert mod.format_number("inf") == "2147483647"

    def test_negative_infinity(self):
        """Return min int."""
        assert mod.format_number("-inf") == "-2147483647"


class TestFormatNumbers:
    def test_empty(self):
        """Return empty list."""
        empty: list[str] = []
        assert list(mod.format_numbers(*empty)) == []

    def test_explicit(self):
        """Return list of formatted strings."""
        assert list(mod.format_numbers(*[1, 2, 3])) == ["1", "2", "3"]


class TestFormatNumbersInString:
    def test_empty(self):
        """Return empty string."""
        assert mod.format_numbers_in_string("") == ""

    def test_no_floats(self):
        """Return the string."""
        assert mod.format_numbers_in_string("abc") == "abc"

    def test_float_in_frong(self):
        """Return the string."""
        assert mod.format_numbers_in_string("3.14abc") == "3.14abc"

    def test_float_in_middle(self):
        """Return the string."""
        assert mod.format_numbers_in_string("abc3.14def") == "abc3.14def"

    def test_float_in_end(self):
        """Return the string."""
        assert mod.format_numbers_in_string("abc3.14") == "abc3.14"

    def test_multiple_floats(self):
        """Return the string."""
        assert mod.format_numbers_in_string("abc3.14def2.718") == "abc3.14def2.718"

    def test_exponential_notation(self):
        """Return the string."""
        assert mod.format_numbers_in_string("3.14159e-10") == "0"

    def test_exponential_notation_big_e(self):
        """Return the string."""
        assert mod.format_numbers_in_string("3.14159E-10") == "0"

    def test_non_default_precision(self):
        """Return the string."""
        assert mod.format_numbers_in_string("3.14159", 3) == "3.142"

    def test_safe_from_leading_e(self):
        """Do not treat e3.14159 as exponential notation."""
        assert mod.format_numbers_in_string("e3.14159", 2) == "e3.14"

    def test_safe_from_trailing_e(self):
        """Do not treat 3.14159e as exponential notation."""
        assert mod.format_numbers_in_string("3.14159e", 2) == "3.14e"
