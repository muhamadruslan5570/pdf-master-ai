# ==========================================================
# PDF MASTER AI
# Rate Limit Middleware
# ==========================================================

# ----------------------------------------------------------
# IMPORT
# ----------------------------------------------------------

from fastapi import FastAPI

from slowapi.errors import RateLimitExceeded

from slowapi.middleware import SlowAPIMiddleware

from core.limiter import limiter

from exceptions.handlers import rate_limit_handler

# ----------------------------------------------------------
# REGISTER RATE LIMIT
# ----------------------------------------------------------

def register_rate_limit(

    app: FastAPI

) -> None:
    """
    Register Rate Limiter Middleware.
    """

    # ------------------------------------------------------
    # LIMITER
    # ------------------------------------------------------

    app.state.limiter = limiter

    # ------------------------------------------------------
    # EXCEPTION
    # ------------------------------------------------------

    app.add_exception_handler(

        RateLimitExceeded,

        rate_limit_handler

    )

    # ------------------------------------------------------
    # MIDDLEWARE
    # ------------------------------------------------------

    app.add_middleware(

        SlowAPIMiddleware

    )