# ==========================================================
# PDF MASTER AI
# Pagination Schema
# ==========================================================

# ----------------------------------------------------------
# IMPORT
# ----------------------------------------------------------

from pydantic import Field

from schemas.base import BaseSchema

# ----------------------------------------------------------
# PAGINATION REQUEST
# ----------------------------------------------------------

class PaginationRequest(BaseSchema):

    page: int = Field(
        default=1,
        ge=1
    )

    per_page: int = Field(
        default=10,
        ge=1,
        le=100
    )

# ----------------------------------------------------------
# PAGINATION RESPONSE
# ----------------------------------------------------------

class PaginationResponse(BaseSchema):

    page: int

    per_page: int

    total_items: int

    total_pages: int