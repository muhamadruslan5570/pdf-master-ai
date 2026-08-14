# ==========================================================
# PDF MASTER AI
# Validators
# ==========================================================

# ----------------------------------------------------------
# IMPORT
# ----------------------------------------------------------

import re
from pathlib import Path

# ----------------------------------------------------------
# EMAIL
# ----------------------------------------------------------

def is_valid_email(email: str) -> bool:

    pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'

    return re.match(pattern, email) is not None

# ----------------------------------------------------------
# USERNAME
# ----------------------------------------------------------

def is_valid_username(username: str) -> bool:

    pattern = r'^[a-zA-Z0-9_.-]{3,100}$'

    return re.match(pattern, username) is not None

# ----------------------------------------------------------
# FILE NAME
# ----------------------------------------------------------

def sanitize_filename(filename: str) -> str:

    filename = Path(filename).name

    filename = filename.replace(" ", "_")

    return filename

# ----------------------------------------------------------
# FILE EXTENSIONS
# ----------------------------------------------------------

ALLOWED_EXTENSIONS = {

    "pdf",

    "doc",

    "docx",

    "xls",

    "xlsx",

    "ppt",

    "pptx",

    "jpg",

    "jpeg",

    "png",

    "gif",

    "bmp",

    "tiff",

    "webp",

    "svg",

    "zip",

    "rar",

    "7z",

    "txt",

    "csv",

    "html",

    "htm"

}

# ----------------------------------------------------------
# CHECK EXTENSION
# ----------------------------------------------------------

def is_allowed_extension(filename: str) -> bool:

    extension = filename.rsplit(".", 1)[-1].lower()

    return extension in ALLOWED_EXTENSIONS

# ----------------------------------------------------------
# MIME TYPES
# ----------------------------------------------------------

ALLOWED_MIME_TYPES = {

    "application/pdf",

    "application/msword",

    "application/vnd.openxmlformats-officedocument.wordprocessingml.document",

    "application/vnd.ms-excel",

    "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",

    "application/vnd.ms-powerpoint",

    "application/vnd.openxmlformats-officedocument.presentationml.presentation",

    "image/jpeg",

    "image/png",

    "image/webp",

    "image/gif",

    "text/plain",

    "text/csv",

    "text/html",

    "application/zip"

}

# ----------------------------------------------------------
# CHECK MIME TYPE
# ----------------------------------------------------------

def is_allowed_mime_type(mime_type: str) -> bool:

    return mime_type in ALLOWED_MIME_TYPES

# ----------------------------------------------------------
# FILE SIZE
# ----------------------------------------------------------

MAX_FILE_SIZE = 1024 * 1024 * 100

# ----------------------------------------------------------
# CHECK FILE SIZE
# ----------------------------------------------------------

def is_allowed_file_size(file_size: int) -> bool:

    return file_size <= MAX_FILE_SIZE