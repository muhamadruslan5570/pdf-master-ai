# ==========================================================
# PDF MASTER AI
# Office Utilities
# ==========================================================

# ----------------------------------------------------------
# IMPORT
# ----------------------------------------------------------

from pathlib import Path

# ----------------------------------------------------------
# WORD
# ----------------------------------------------------------

WORD_EXTENSIONS = {

    ".doc",

    ".docx"

}

# ----------------------------------------------------------
# EXCEL
# ----------------------------------------------------------

EXCEL_EXTENSIONS = {

    ".xls",

    ".xlsx"

}

# ----------------------------------------------------------
# POWERPOINT
# ----------------------------------------------------------

POWERPOINT_EXTENSIONS = {

    ".ppt",

    ".pptx"

}

# ----------------------------------------------------------
# ALL OFFICE
# ----------------------------------------------------------

OFFICE_EXTENSIONS = (

    WORD_EXTENSIONS

    | EXCEL_EXTENSIONS

    | POWERPOINT_EXTENSIONS

)

# ----------------------------------------------------------
# WORD
# ----------------------------------------------------------

def is_word(

    file_path: str

) -> bool:
    """
    Check Word document.
    """

    return (

        Path(file_path)

        .suffix

        .lower()

        in WORD_EXTENSIONS

    )

# ----------------------------------------------------------
# EXCEL
# ----------------------------------------------------------

def is_excel(

    file_path: str

) -> bool:
    """
    Check Excel document.
    """

    return (

        Path(file_path)

        .suffix

        .lower()

        in EXCEL_EXTENSIONS

    )

# ----------------------------------------------------------
# POWERPOINT
# ----------------------------------------------------------

def is_powerpoint(

    file_path: str

) -> bool:
    """
    Check PowerPoint document.
    """

    return (

        Path(file_path)

        .suffix

        .lower()

        in POWERPOINT_EXTENSIONS

    )

# ----------------------------------------------------------
# OFFICE
# ----------------------------------------------------------

def is_office(

    file_path: str

) -> bool:
    """
    Check Office document.
    """

    return (

        Path(file_path)

        .suffix

        .lower()

        in OFFICE_EXTENSIONS

    )

# ----------------------------------------------------------
# DOCUMENT TYPE
# ----------------------------------------------------------

def get_office_type(

    file_path: str

) -> str:

    if is_word(file_path):

        return "word"

    if is_excel(file_path):

        return "excel"

    if is_powerpoint(file_path):

        return "powerpoint"

    return "unknown"

# ----------------------------------------------------------
# EXTENSION
# ----------------------------------------------------------

def get_extension(

    file_path: str

) -> str:

    return (

        Path(file_path)

        .suffix

        .lower()

    )

# ----------------------------------------------------------
# FILE NAME
# ----------------------------------------------------------

def get_filename(

    file_path: str

) -> str:

    return (

        Path(file_path)

        .name

    )

# ----------------------------------------------------------
# FILE STEM
# ----------------------------------------------------------

def get_stem(

    file_path: str

) -> str:

    return (

        Path(file_path)

        .stem

    )