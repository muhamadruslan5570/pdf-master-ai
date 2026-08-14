# ==========================================================
# PDF MASTER AI
# Validator Utilities
# ==========================================================

# ----------------------------------------------------------
# IMPORT
# ----------------------------------------------------------

from typing import Any

# ----------------------------------------------------------
# EMPTY
# ----------------------------------------------------------

def is_empty(value: Any) -> bool:
    """
    Check whether value is empty.
    """

    return value in (

        None,

        "",

        [],

        {},

        ()

    )

# ----------------------------------------------------------
# NOT EMPTY
# ----------------------------------------------------------

def is_not_empty(value: Any) -> bool:
    """
    Check whether value is not empty.
    """

    return not is_empty(value)

# ----------------------------------------------------------
# POSITIVE NUMBER
# ----------------------------------------------------------

def is_positive(value: int | float) -> bool:
    """
    Check positive number.
    """

    return value > 0

# ----------------------------------------------------------
# NON NEGATIVE
# ----------------------------------------------------------

def is_non_negative(value: int | float) -> bool:
    """
    Check non negative number.
    """

    return value >= 0

# ----------------------------------------------------------
# IN RANGE
# ----------------------------------------------------------

def in_range(

    value: int | float,

    minimum: int | float,

    maximum: int | float

) -> bool:
    """
    Check value range.
    """

    return minimum <= value <= maximum

# ----------------------------------------------------------
# STRING
# ----------------------------------------------------------

def is_string(value: Any) -> bool:
    """
    Check string.
    """

    return isinstance(value, str)

# ----------------------------------------------------------
# INTEGER
# ----------------------------------------------------------

def is_integer(value: Any) -> bool:
    """
    Check integer.
    """

    return isinstance(value, int)

# ----------------------------------------------------------
# FLOAT
# ----------------------------------------------------------

def is_float(value: Any) -> bool:
    """
    Check float.
    """

    return isinstance(value, float)

# ----------------------------------------------------------
# BOOLEAN
# ----------------------------------------------------------

def is_boolean(value: Any) -> bool:
    """
    Check boolean.
    """

    return isinstance(value, bool)

# ----------------------------------------------------------
# LIST
# ----------------------------------------------------------

def is_list(value: Any) -> bool:
    """
    Check list.
    """

    return isinstance(value, list)

# ----------------------------------------------------------
# DICTIONARY
# ----------------------------------------------------------

def is_dict(value: Any) -> bool:
    """
    Check dictionary.
    """

    return isinstance(value, dict)

# ----------------------------------------------------------
# MIN LENGTH
# ----------------------------------------------------------

def min_length(

    value: str,

    length: int

) -> bool:
    """
    Check minimum length.
    """

    return len(value) >= length

# ----------------------------------------------------------
# MAX LENGTH
# ----------------------------------------------------------

def max_length(

    value: str,

    length: int

) -> bool:
    """
    Check maximum length.
    """

    return len(value) <= length

# ----------------------------------------------------------
# BETWEEN LENGTH
# ----------------------------------------------------------

def between_length(

    value: str,

    minimum: int,

    maximum: int

) -> bool:
    """
    Check string length.
    """

    return minimum <= len(value) <= maximum