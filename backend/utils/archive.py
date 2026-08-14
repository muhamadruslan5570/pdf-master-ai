# ==========================================================
# PDF MASTER AI
# Archive Utilities
# ==========================================================

# ----------------------------------------------------------
# IMPORT
# ----------------------------------------------------------

import zipfile

from pathlib import Path

# ----------------------------------------------------------
# ARCHIVE EXTENSIONS
# ----------------------------------------------------------

ARCHIVE_EXTENSIONS = {

    ".zip",

    ".rar",

    ".7z",

    ".tar",

    ".gz"

}

# ----------------------------------------------------------
# IS ARCHIVE
# ----------------------------------------------------------

def is_archive(

    file_path: str

) -> bool:
    """
    Check archive file.
    """

    return (

        Path(file_path)

        .suffix

        .lower()

        in ARCHIVE_EXTENSIONS

    )

# ----------------------------------------------------------
# ZIP FILE
# ----------------------------------------------------------

def is_zip(

    file_path: str

) -> bool:
    """
    Check ZIP archive.
    """

    return (

        Path(file_path)

        .suffix

        .lower()

        == ".zip"

    )

# ----------------------------------------------------------
# FILE LIST
# ----------------------------------------------------------

def list_zip_files(

    file_path: str

) -> list[str]:
    """
    List all files inside ZIP archive.
    """

    with zipfile.ZipFile(

        file_path,

        "r"

    ) as archive:

        return archive.namelist()

# ----------------------------------------------------------
# EXTRACT ZIP
# ----------------------------------------------------------

def extract_zip(

    file_path: str,

    output_directory: str

) -> None:
    """
    Extract ZIP archive.
    """

    with zipfile.ZipFile(

        file_path,

        "r"

    ) as archive:

        archive.extractall(

            output_directory

        )

# ----------------------------------------------------------
# CREATE ZIP
# ----------------------------------------------------------

def create_zip(

    source_directory: str,

    output_zip: str

) -> None:
    """
    Create ZIP archive.
    """

    source = Path(

        source_directory

    )

    with zipfile.ZipFile(

        output_zip,

        "w",

        compression=zipfile.ZIP_DEFLATED

    ) as archive:

        for file in source.rglob("*"):

            if file.is_file():

                archive.write(

                    file,

                    arcname=file.relative_to(source)

                )

# ----------------------------------------------------------
# ZIP INFO
# ----------------------------------------------------------

def get_zip_info(

    file_path: str

) -> dict:
    """
    Get ZIP information.
    """

    with zipfile.ZipFile(

        file_path,

        "r"

    ) as archive:

        return {

            "total_files": len(

                archive.infolist()

            ),

            "comment": archive.comment.decode(

                errors="ignore"

            )

        }