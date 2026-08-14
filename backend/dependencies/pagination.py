# ==========================================================
# PDF MASTER AI
# Pagination Dependency
# ==========================================================

# ----------------------------------------------------------
# IMPORT
# ----------------------------------------------------------

from typing import TypedDict

from fastapi import Query

# ----------------------------------------------------------
# PAGINATION TYPE
# ----------------------------------------------------------

class PaginationParams(TypedDict):

    page: int

    per_page: int

    skip: int

    limit: int

# ----------------------------------------------------------
# PAGINATION
# ----------------------------------------------------------

def pagination(

    page: int = Query(

        default=1,

        ge=1,

        description="Current page"

    ),

    per_page: int = Query(

        default=10,

        ge=1,

        le=100,

        description="Items per page"

    )

) -> PaginationParams:

    """
    Pagination dependency.

    Returns:
        {
            page,
            per_page,
            skip,
            limit
        }
    """

    skip = (page - 1) * per_page

    return {

        "page": page,

        "per_page": per_page,

        "skip": skip,

        "limit": per_page

    }