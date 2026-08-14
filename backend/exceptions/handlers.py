# ==========================================================
# PDF MASTER AI
# Global Exception Handlers
# ==========================================================

# ----------------------------------------------------------
# IMPORT
# ----------------------------------------------------------

from fastapi import (
    FastAPI,
    Request,
    HTTPException
)

from fastapi.responses import JSONResponse

from fastapi.exceptions import RequestValidationError

from sqlalchemy.exc import SQLAlchemyError

from slowapi.errors import RateLimitExceeded

from core.logger import error

# ----------------------------------------------------------
# HTTP EXCEPTION
# ----------------------------------------------------------

async def http_exception_handler(

    request: Request,

    exc: HTTPException

):

    error(

        f"HTTPException: {exc.detail}"

    )

    return JSONResponse(

        status_code=exc.status_code,

        content={

            "success": False,

            "error": exc.detail,

            "status_code": exc.status_code

        }

    )

# ----------------------------------------------------------
# VALIDATION ERROR
# ----------------------------------------------------------

async def validation_exception_handler(

    request: Request,

    exc: RequestValidationError

):

    error(

        f"ValidationError: {exc.errors()}"

    )

    return JSONResponse(

        status_code=422,

        content={

            "success": False,

            "error": "Validation Error",

            "details": exc.errors(),

            "status_code": 422

        }

    )

# ----------------------------------------------------------
# DATABASE ERROR
# ----------------------------------------------------------

async def sqlalchemy_exception_handler(

    request: Request,

    exc: SQLAlchemyError

):

    error(

        f"DatabaseError: {str(exc)}"

    )

    return JSONResponse(

        status_code=500,

        content={

            "success": False,

            "error": "Database Error",

            "status_code": 500

        }

    )

# ----------------------------------------------------------
# RATE LIMIT
# ----------------------------------------------------------

async def rate_limit_handler(

    request: Request,

    exc: RateLimitExceeded

):

    error(

        "Rate Limit Exceeded"

    )

    return JSONResponse(

        status_code=429,

        content={

            "success": False,

            "error": "Too Many Requests",

            "status_code": 429

        }

    )

# ----------------------------------------------------------
# UNKNOWN ERROR
# ----------------------------------------------------------

async def global_exception_handler(

    request: Request,

    exc: Exception

):

    error(

        f"Unhandled Exception: {str(exc)}"

    )

    return JSONResponse(

        status_code=500,

        content={

            "success": False,

            "error": "Internal Server Error",

            "status_code": 500

        }

    )

# ----------------------------------------------------------
# REGISTER HANDLERS
# ----------------------------------------------------------

def register_exception_handlers(

    app: FastAPI

):

    app.add_exception_handler(

        HTTPException,

        http_exception_handler

    )

    app.add_exception_handler(

        RequestValidationError,

        validation_exception_handler

    )

    app.add_exception_handler(

        SQLAlchemyError,

        sqlalchemy_exception_handler

    )

    app.add_exception_handler(

        RateLimitExceeded,

        rate_limit_handler

    )

    app.add_exception_handler(

        Exception,

        global_exception_handler

    )