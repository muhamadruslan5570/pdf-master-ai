# ==========================================================
# PDF MASTER AI
# Common Schemas
# ==========================================================

# ----------------------------------------------------------
# IMPORT
# ----------------------------------------------------------

from typing import Any

from pydantic import Field

from schemas.base import BaseSchema

# ----------------------------------------------------------
# MESSAGE RESPONSE
# ----------------------------------------------------------

class MessageResponse(BaseSchema):

    message: str

# ----------------------------------------------------------
# SUCCESS RESPONSE
# ----------------------------------------------------------

class SuccessResponse(BaseSchema):

    success: bool = True

    message: str

# ----------------------------------------------------------
# ERROR RESPONSE
# ----------------------------------------------------------

class ErrorResponse(BaseSchema):

    success: bool = False

    message: str

# ----------------------------------------------------------
# PAGINATION
# ----------------------------------------------------------

class Pagination(BaseSchema):

    page: int = Field(default=1, ge=1)

    per_page: int = Field(default=10, ge=1, le=100)

# ----------------------------------------------------------
# API RESPONSE
# ----------------------------------------------------------

class APIResponse(BaseSchema):

    success: bool = True

    message: str

    data: Any | None = None