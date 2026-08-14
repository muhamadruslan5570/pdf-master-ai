# ==========================================================
# PDF MASTER AI
# Response Utilities
# ==========================================================

# ----------------------------------------------------------
# IMPORT
# ----------------------------------------------------------

from typing import Any

from fastapi.responses import JSONResponse

# ----------------------------------------------------------
# SUCCESS RESPONSE
# ----------------------------------------------------------

def success_response(

    data: Any = None,

    message: str = "Success",

    status_code: int = 200

) -> JSONResponse:
    """
    Standard success response.
    """

    return JSONResponse(

        status_code=status_code,

        content={

            "success": True,

            "message": message,

            "data": data

        }

    )

# ----------------------------------------------------------
# ERROR RESPONSE
# ----------------------------------------------------------

def error_response(

    message: str = "Error",

    status_code: int = 400,

    errors: Any = None

) -> JSONResponse:
    """
    Standard error response.
    """

    return JSONResponse(

        status_code=status_code,

        content={

            "success": False,

            "message": message,

            "errors": errors

        }

    )

# ----------------------------------------------------------
# PAGINATION RESPONSE
# ----------------------------------------------------------

def paginated_response(

    data: list,

    total: int,

    page: int,

    per_page: int,

    message: str = "Success"

) -> JSONResponse:
    """
    Standard pagination response.
    """

    total_pages = (

        total + per_page - 1

    ) // per_page

    return JSONResponse(

        status_code=200,

        content={

            "success": True,

            "message": message,

            "data": data,

            "pagination": {

                "total": total,

                "page": page,

                "per_page": per_page,

                "total_pages": total_pages,

                "has_next": page < total_pages,

                "has_previous": page > 1

            }

        }

    )

# ----------------------------------------------------------
# CREATED RESPONSE
# ----------------------------------------------------------

def created_response(

    data: Any,

    message: str = "Created Successfully"

) -> JSONResponse:
    """
    HTTP 201 Created response.
    """

    return success_response(

        data=data,

        message=message,

        status_code=201

    )

# ----------------------------------------------------------
# NO CONTENT RESPONSE
# ----------------------------------------------------------

def no_content_response() -> JSONResponse:
    """
    HTTP 204 No Content response.
    """

    return JSONResponse(

        status_code=204,

        content=None

    )