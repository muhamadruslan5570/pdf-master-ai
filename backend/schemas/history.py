# ==========================================================
# PDF MASTER AI
# History Schemas
# ==========================================================

# ----------------------------------------------------------
# IMPORT
# ----------------------------------------------------------

from datetime import datetime
from enum import Enum

from pydantic import Field

from schemas.base import BaseSchema

# ----------------------------------------------------------
# HISTORY CATEGORY
# ----------------------------------------------------------

class HistoryCategory(str, Enum):

    PDF = "pdf"

    CONVERT = "convert"

    IMAGE = "image"

    OFFICE = "office"

    ARCHIVE = "archive"

    AI = "ai"

    UTILITIES = "utilities"


# ----------------------------------------------------------
# HISTORY ACTION
# ----------------------------------------------------------

class HistoryAction(str, Enum):

    COMPRESS_PDF = "compress_pdf"

    MERGE_PDF = "merge_pdf"

    SPLIT_PDF = "split_pdf"

    ROTATE_PDF = "rotate_pdf"

    ORGANIZE_PDF = "organize_pdf"

    DELETE_PAGES = "delete_pages"

    EXTRACT_PAGES = "extract_pages"

    WATERMARK_PDF = "watermark_pdf"

    PROTECT_PDF = "protect_pdf"

    UNLOCK_PDF = "unlock_pdf"

    REPAIR_PDF = "repair_pdf"

    SIGN_PDF = "sign_pdf"

    OCR_PDF = "ocr_pdf"

    PDF_TO_WORD = "pdf_to_word"

    PDF_TO_EXCEL = "pdf_to_excel"

    PDF_TO_POWERPOINT = "pdf_to_powerpoint"

    PDF_TO_JPG = "pdf_to_jpg"

    PDF_TO_PNG = "pdf_to_png"

    PDF_TO_WEBP = "pdf_to_webp"

    WORD_TO_PDF = "word_to_pdf"

    EXCEL_TO_PDF = "excel_to_pdf"

    POWERPOINT_TO_PDF = "powerpoint_to_pdf"

    JPG_TO_PDF = "jpg_to_pdf"

    PNG_TO_PDF = "png_to_pdf"

    WEBP_TO_PDF = "webp_to_pdf"

    COMPRESS_IMAGE = "compress_image"

    RESIZE_IMAGE = "resize_image"

    CROP_IMAGE = "crop_image"

    REMOVE_BACKGROUND = "remove_background"

    IMAGE_UPSCALER = "image_upscaler"

    IMAGE_TO_TEXT = "image_to_text"

    CHAT_WITH_PDF = "chat_with_pdf"

    SUMMARIZE_DOCUMENT = "summarize_document"

    TRANSLATE_DOCUMENT = "translate_document"

    AI_WRITER = "ai_writer"


# ----------------------------------------------------------
# HISTORY STATUS
# ----------------------------------------------------------

class HistoryStatus(str, Enum):

    PENDING = "pending"

    PROCESSING = "processing"

    COMPLETED = "completed"

    FAILED = "failed"

    CANCELLED = "cancelled"


# ----------------------------------------------------------
# HISTORY BASE
# ----------------------------------------------------------

class HistoryBase(BaseSchema):

    action: HistoryAction

    category: HistoryCategory

    message: str | None = None


# ----------------------------------------------------------
# CREATE HISTORY
# ----------------------------------------------------------

class HistoryCreate(HistoryBase):

    user_id: int

    file_id: int


# ----------------------------------------------------------
# UPDATE HISTORY
# ----------------------------------------------------------

class HistoryUpdate(BaseSchema):

    status: HistoryStatus | None = None

    result_file: str | None = None

    message: str | None = None


# ----------------------------------------------------------
# HISTORY DETAIL
# ----------------------------------------------------------

class HistoryDetail(HistoryBase):

    id: int

    user_id: int

    file_id: int

    status: HistoryStatus

    result_file: str | None

    created_at: datetime

    updated_at: datetime


# ----------------------------------------------------------
# HISTORY RESPONSE
# ----------------------------------------------------------

class HistoryResponse(BaseSchema):

    success: bool = True

    message: str

    data: HistoryDetail


# ----------------------------------------------------------
# HISTORY LIST RESPONSE
# ----------------------------------------------------------

class HistoryListResponse(BaseSchema):

    success: bool = True

    total: int

    histories: list[HistoryDetail]