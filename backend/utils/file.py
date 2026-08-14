# ==========================================================
# PDF MASTER AI
# File Utilities
# ==========================================================

# ----------------------------------------------------------
# IMPORT
# ----------------------------------------------------------

import os
import shutil
import mimetypes
from pathlib import Path
from uuid import uuid4

# ----------------------------------------------------------
# CREATE DIRECTORY
# ----------------------------------------------------------

def create_directory(

    directory: str

) -> None:
    """
    Create directory if it does not exist.
    """

    Path(directory).mkdir(

        parents=True,

        exist_ok=True

    )

# ----------------------------------------------------------
# DIRECTORY EXISTS
# ----------------------------------------------------------

def directory_exists(

    directory: str

) -> bool:
    """
    Check directory exists.
    """

    return Path(directory).exists()

# ----------------------------------------------------------
# FILE EXISTS
# ----------------------------------------------------------

def file_exists(

    file_path: str

) -> bool:
    """
    Check file exists.
    """

    return Path(file_path).is_file()

# ----------------------------------------------------------
# DELETE FILE
# ----------------------------------------------------------

def delete_file(

    file_path: str

) -> bool:
    """
    Delete file.
    """

    path = Path(file_path)

    if path.exists():

        path.unlink()

        return True

    return False

# ----------------------------------------------------------
# DELETE DIRECTORY
# ----------------------------------------------------------

def delete_directory(

    directory: str

) -> bool:
    """
    Delete directory.
    """

    path = Path(directory)

    if path.exists():

        shutil.rmtree(path)

        return True

    return False

# ----------------------------------------------------------
# COPY FILE
# ----------------------------------------------------------

def copy_file(

    source: str,

    destination: str

) -> None:
    """
    Copy file.
    """

    shutil.copy2(

        source,

        destination

    )

# ----------------------------------------------------------
# MOVE FILE
# ----------------------------------------------------------

def move_file(

    source: str,

    destination: str

) -> None:
    """
    Move file.
    """

    shutil.move(

        source,

        destination

    )

# ----------------------------------------------------------
# RENAME FILE
# ----------------------------------------------------------

def rename_file(

    source: str,

    destination: str

) -> None:
    """
    Rename file.
    """

    os.rename(

        source,

        destination

    )

# ----------------------------------------------------------
# FILE SIZE
# ----------------------------------------------------------

def get_file_size(

    file_path: str

) -> int:
    """
    Get file size.
    """

    return os.path.getsize(

        file_path

    )

# ----------------------------------------------------------
# FILE EXTENSION
# ----------------------------------------------------------

def get_extension(

    filename: str

) -> str:
    """
    Get extension.
    """

    return Path(

        filename

    ).suffix.lower()

# ----------------------------------------------------------
# FILE NAME
# ----------------------------------------------------------

def get_filename(

    file_path: str

) -> str:
    """
    Get filename.
    """

    return Path(

        file_path

    ).name

# ----------------------------------------------------------
# FILE STEM
# ----------------------------------------------------------

def get_stem(

    file_path: str

) -> str:
    """
    Filename without extension.
    """

    return Path(

        file_path

    ).stem

# ----------------------------------------------------------
# MIME TYPE
# ----------------------------------------------------------

def get_mime_type(

    file_path: str

) -> str | None:
    """
    Detect mime type.
    """

    mime_type, _ = mimetypes.guess_type(

        file_path

    )

    return mime_type

# ----------------------------------------------------------
# UNIQUE FILE NAME
# ----------------------------------------------------------

def generate_unique_filename(

    extension: str

) -> str:
    """
    Generate unique filename.
    """

    extension = extension.replace(

        ".",

        ""

    )

    return f"{uuid4().hex}.{extension}"