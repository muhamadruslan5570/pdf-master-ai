# ==========================================================
# PDF MASTER AI
# Helper Utilities
# ==========================================================

# ----------------------------------------------------------
# IMPORT
# ----------------------------------------------------------

import uuid

from datetime import (
    datetime,
    timezone
)

# ----------------------------------------------------------
# UUID
# ----------------------------------------------------------

def generate_uuid() -> str:
    """
    Generate UUID v4.
    """

    return str(uuid.uuid4())

# ----------------------------------------------------------
# UTC NOW
# ----------------------------------------------------------

def utc_now() -> datetime:
    """
    Get current UTC datetime.
    """

    return datetime.now(
        timezone.utc
    )

# ----------------------------------------------------------
# TIMESTAMP
# ----------------------------------------------------------

def current_timestamp() -> int:
    """
    Get current Unix timestamp.
    """

    return int(

        utc_now().timestamp()

    )

# ----------------------------------------------------------
# BOOLEAN
# ----------------------------------------------------------

def to_bool(value) -> bool:
    """
    Convert value to boolean.
    """

    if isinstance(value, bool):

        return value

    return str(value).strip().lower() in (

        "true",

        "1",

        "yes",

        "y",

        "on"

    )

# ----------------------------------------------------------
# BYTES
# ----------------------------------------------------------

def bytes_to_mb(

    size: int

) -> float:
    """
    Convert bytes to MB.
    """

    return round(

        size / (1024 * 1024),

        2

    )

# ----------------------------------------------------------
# MB
# ----------------------------------------------------------

def mb_to_bytes(

    size: int

) -> int:
    """
    Convert MB to bytes.
    """

    return size * 1024 * 1024

# ----------------------------------------------------------
# CLAMP
# ----------------------------------------------------------

def clamp(

    value: int,

    minimum: int,

    maximum: int

) -> int:
    """
    Limit value between minimum and maximum.
    """

    return max(

        minimum,

        min(

            value,

            maximum

        )

    )

# ----------------------------------------------------------
# EMPTY
# ----------------------------------------------------------

def is_empty(

    value

) -> bool:
    """
    Check whether a value is empty.
    """

    return value in (

        None,

        "",

        [],

        {},

        ()

    )

# ----------------------------------------------------------
# SLUG
# ----------------------------------------------------------

def slugify(

    text: str

) -> str:
    """
    Convert text to slug.
    """

    return (

        text.strip()

        .lower()

        .replace(" ", "-")

        .replace("_", "-")

    )