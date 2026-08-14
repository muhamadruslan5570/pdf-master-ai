# ==========================================================
# PDF MASTER AI
# File Schemas
# ==========================================================

# ----------------------------------------------------------
# IMPORT
# ----------------------------------------------------------

from datetime import datetime
from enum import Enum

from pydantic import Field

from schemas.base import BaseSchema

# ----------------------------------------------------------
# FILE STATUS
# ----------------------------------------------------------

class FileStatus(str, Enum):

    UPLOADED = "uploaded"

    PROCESSING = "processing"

    COMPLETED = "completed"

    FAILED = "failed"

    DELETED = "deleted"


# ----------------------------------------------------------
# FILE CATEGORY
# ----------------------------------------------------------

class FileCategory(str, Enum):

    PDF = "pdf"

    IMAGE = "image"

    WORD = "word"

    EXCEL = "excel"

    POWERPOINT = "powerpoint"

    ARCHIVE = "archive"

    OTHER = "other"


# ----------------------------------------------------------
# FILE BASE
# ----------------------------------------------------------

class FileBase(BaseSchema):

    original_name: str = Field(
        min_length=1,
        max_length=255
    )

    description: str | None = None


# ----------------------------------------------------------
# CREATE FILE
# ----------------------------------------------------------

class FileCreate(FileBase):

    user_id: int


# ----------------------------------------------------------
# UPDATE FILE
# ----------------------------------------------------------

class FileUpdate(BaseSchema):

    description: str | None = None

    status: FileStatus | None = None


# ----------------------------------------------------------
# FILE DETAIL
# ----------------------------------------------------------

class FileDetail(FileBase):

    id: int

    user_id: int

    stored_name: str

    file_extension: str

    mime_type: str

    file_size: int

    category: FileCategory

    storage_path: str

    public_url: str | None

    status: FileStatus

    created_at: datetime

    updated_at: datetime


# ----------------------------------------------------------
# FILE RESPONSE
# ----------------------------------------------------------

class FileResponse(BaseSchema):

    success: bool = True

    message: str

    data: FileDetail


# ----------------------------------------------------------
# FILE LIST RESPONSE
# ----------------------------------------------------------

class FileListResponse(BaseSchema):

    success: bool = True

    total: int

    files: list[FileDetail]