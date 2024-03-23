"""Test functions in docx2python.numbering_formats.py

:author: Shay Hill
:created: 6/26/2019
"""

import pytest

from numstr import counting as mod


class TestLowerLetter:
    """Test numbering_formats.lower_letters"""

    def test_convert_positive_int(self) -> None:
        """Convert a positive integer to a string of letters"""
        assert mod.lower_letters(1) == "a"
        assert mod.lower_letters(26) == "z"
        assert mod.lower_letters(27) == "aa"

    def test_zero(self) -> None:
        """Raise a value error for < 1"""
        with pytest.raises(ValueError) as msg:
            _ = mod.lower_letters(0)
        assert "0 and <1 are not defined" in str(msg.value)

    def test_neg(self) -> None:
        """Raise a value error for < 1"""
        with pytest.raises(ValueError) as msg:
            _ = mod.lower_letters(-1)
        assert "0 and <1 are not defined" in str(msg.value)


def test_upper_letters(positive_ints: int) -> None:
    """Same as lower_letters, but upper"""
    assert mod.upper_letters(positive_ints) == mod.lower_letters(positive_ints).upper()


class TestLowerRoman:
    """Test numbering_formats.lower_roman"""

    def test_convert_positive_int(self, roman_1_to_3999: tuple[int, str]) -> None:
        """Convert a positive integer to a string of letters"""
        arabic, roman = roman_1_to_3999
        assert mod.lower_roman(arabic) == roman

    def test_zero(self) -> None:
        """Raise a value error for < 1"""
        with pytest.raises(ValueError) as msg:
            _ = mod.lower_roman(0)
        assert "Roman" in str(msg.value)

    def test_neg(self) -> None:
        """Raise a value error for < 1"""
        with pytest.raises(ValueError) as msg:
            _ = mod.lower_roman(-1)
        assert "Roman" in str(msg.value)

class TestFromRoman:
    """Test conversion from Roman numerals"""

    def test_lower(self, roman_1_to_3999: tuple[int, str]) -> None:
        """Convert a Roman numeral to an integer"""
        arabic, roman = roman_1_to_3999
        assert mod.get_int_from_roman(roman) == arabic

    def test_upper(self, roman_1_to_3999: tuple[int, str]) -> None:
        """Convert a Roman numeral to an integer"""
        arabic, roman = roman_1_to_3999
        assert mod.get_int_from_roman(roman.upper()) == arabic

class TestFromLetter:
    """Test conversion from letters"""

    def test_lower(self, positive_ints: int) -> None:
        """Convert a letter to an integer"""
        letters = mod.lower_letters(positive_ints)
        assert mod.get_int_from_letters(letters) == positive_ints

    def test_upper(self, positive_ints: int) -> None:
        """Convert a letter to an integer"""
        base26letters = mod.lower_letters(positive_ints)
        assert mod.get_int_from_letters(base26letters) == positive_ints


def test_upper_roman(positive_ints: int) -> None:
    """Same as lower_roman, but upper"""
    assert mod.upper_roman(positive_ints) == mod.lower_roman(positive_ints).upper()
