# ==========================================================
# PDF MASTER AI
# PDF Utilities
# ==========================================================

# ----------------------------------------------------------
# IMPORT
# ----------------------------------------------------------

from pathlib import Path

from pypdf import PdfReader

# ----------------------------------------------------------
# PDF EXISTS
# ----------------------------------------------------------

def is_pdf(

    file_path: str

) -> bool:
    """
    Check PDF extension.
    """

    return Path(

        file_path

    ).suffix.lower() == ".pdf"

# ----------------------------------------------------------
# PAGE COUNT
# ----------------------------------------------------------

def get_page_count(

    file_path: str

) -> int:
    """
    Get total PDF pages.
    """

    reader = PdfReader(

        file_path

    )

    return len(

        reader.pages

    )

# ----------------------------------------------------------
# PDF ENCRYPTED
# ----------------------------------------------------------

def is_encrypted(

    file_path: str

) -> bool:
    """
    Check encrypted PDF.
    """

    reader = PdfReader(

        file_path

    )

    return reader.is_encrypted

# ----------------------------------------------------------
# PDF METADATA
# ----------------------------------------------------------

def get_metadata(

    file_path: str

) -> dict:
    """
    Get PDF metadata.
    """

    reader = PdfReader(

        file_path

    )

    metadata = reader.metadata

    if metadata is None:

        return {}

    return dict(metadata)

# ----------------------------------------------------------
# PDF TITLE
# ----------------------------------------------------------

def get_title(

    file_path: str

) -> str | None:
    """
    Get PDF title.
    """

    return get_metadata(

        file_path

    ).get("/Title")

# ----------------------------------------------------------
# PDF AUTHOR
# ----------------------------------------------------------

def get_author(

    file_path: str

) -> str | None:
    """
    Get PDF author.
    """

    return get_metadata(

        file_path

    ).get("/Author")

# ----------------------------------------------------------
# PDF SUBJECT
# ----------------------------------------------------------

def get_subject(

    file_path: str

) -> str | None:
    """
    Get PDF subject.
    """

    return get_metadata(

        file_path

    ).get("/Subject")

# ----------------------------------------------------------
# PDF CREATOR
# ----------------------------------------------------------

def get_creator(

    file_path: str

) -> str | None:
    """
    Get PDF creator.
    """

    return get_metadata(

        file_path

    ).get("/Creator")

# ----------------------------------------------------------
# PDF PRODUCER
# ----------------------------------------------------------

def get_producer(

    file_path: str

) -> str | None:
    """
    Get PDF producer.
    """

    return get_metadata(

        file_path

    ).get("/Producer")