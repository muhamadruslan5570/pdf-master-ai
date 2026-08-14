# ==========================================================
# PDF MASTER AI
# Formatter Utilities
# ==========================================================

# ----------------------------------------------------------
# IMPORT
# ----------------------------------------------------------

from datetime import datetime

# ----------------------------------------------------------
# FILE SIZE
# ----------------------------------------------------------

def format_file_size(

    size: int

) -> str:
    """
    Format bytes to human readable size.
    """

    units = [

        "B",

        "KB",

        "MB",

        "GB",

        "TB"

    ]

    size = float(size)

    for unit in units:

        if size < 1024:

            return f"{size:.2f} {unit}"

        size /= 1024

    return f"{size:.2f} PB"

# ----------------------------------------------------------
# DATE
# ----------------------------------------------------------

def format_date(

    value: datetime

) -> str:
    """
    Format date.
    """

    return value.strftime(

        "%Y-%m-%d"

    )

# ----------------------------------------------------------
# DATETIME
# ----------------------------------------------------------

def format_datetime(

    value: datetime

) -> str:
    """
    Format datetime.
    """

    return value.strftime(

        "%Y-%m-%d %H:%M:%S"

    )

# ----------------------------------------------------------
# CURRENCY
# ----------------------------------------------------------

def format_currency(

    amount: float,

    currency: str = "IDR"

) -> str:
    """
    Format currency.
    """

    if currency.upper() == "IDR":

        return f"Rp {amount:,.0f}"

    return f"{currency.upper()} {amount:,.2f}"

# ----------------------------------------------------------
# PERCENTAGE
# ----------------------------------------------------------

def format_percentage(

    value: float

) -> str:
    """
    Format percentage.
    """

    return f"{value:.2f}%"

# ----------------------------------------------------------
# DURATION
# ----------------------------------------------------------

def format_duration(

    seconds: int

) -> str:
    """
    Format seconds to HH:MM:SS.
    """

    hours = seconds // 3600

    minutes = (

        seconds % 3600

    ) // 60

    seconds = seconds % 60

    return (

        f"{hours:02d}:"

        f"{minutes:02d}:"

        f"{seconds:02d}"

    )

# ----------------------------------------------------------
# BOOLEAN
# ----------------------------------------------------------

def format_boolean(

    value: bool

) -> str:
    """
    Format boolean.
    """

    return "Yes" if value else "No"

# ----------------------------------------------------------
# TITLE
# ----------------------------------------------------------

def title_case(

    text: str

) -> str:
    """
    Convert to title case.
    """

    return text.title()

# ----------------------------------------------------------
# UPPER
# ----------------------------------------------------------

def upper_case(

    text: str

) -> str:
    """
    Convert to upper case.
    """

    return text.upper()

# ----------------------------------------------------------
# LOWER
# ----------------------------------------------------------

def lower_case(

    text: str

) -> str:
    """
    Convert to lower case.
    """

    return text.lower()