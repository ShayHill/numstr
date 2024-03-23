# numstr

Convert numbers to strings, limiting precision and removing extra characters.

## SVG float strings

Creates float strings that are appropiate for SVG and other file formats where precision is limited; floats and ints are interchangeable; exponential notation is not supported; and file size is important.

* reduce floating-point precision to ndigits (default 6)
* remove trailing zeros
* remove trailing decimal point (floats == int(num) will be printed as ints)
* convert "-0" to "0"
* clip values `-max_32_bit_signed_int <= num <= max_32_bit_signed_int`

```
NDIGITS  # default 6 precision for floats

extract_float_strings("a2b3")  # "a{}b{}", (2, 3)

extract_floats("a2b3")  # "a{}b{}", (2.0, 3.0)

format_numbers(1/3, 2/3)  # ("0.333333", "0.666667")

format_numbers_in_string("a2.1000001b3e1")  # "a2.1b30"

map_numbers_in_string(int, "a2.0000001b3e1")  # "a2b30", (2, 30)
```

## Outline strings

Convert to and from Roman numerals and Excel-style column names.

```
get_int_from_letters("AB")  # 28

get_int_from_roman("XXVIII")  # 28

lower_letters(28)  # "ab"

lower_roman(28)  # "xxviii"

upper_letters(28)  # "AB"

upper_roman(28)  # "XXVIII"
```
