# ==========================================================
# PDF MASTER AI
# Security Middleware
# ==========================================================

# ----------------------------------------------------------
# IMPORT
# ----------------------------------------------------------

from fastapi import (
    FastAPI,
    Request
)

from starlette.middleware.base import (

    BaseHTTPMiddleware

)

# ----------------------------------------------------------
# SECURITY MIDDLEWARE
# ----------------------------------------------------------

class SecurityMiddleware(

    BaseHTTPMiddleware

):

    async def dispatch(

        self,

        request: Request,

        call_next

    ):

        response = await call_next(

            request

        )

        # --------------------------------------------------
        # SECURITY HEADERS
        # --------------------------------------------------

        response.headers[

            "X-Content-Type-Options"

        ] = "nosniff"

        response.headers[

            "X-Frame-Options"

        ] = "DENY"

        response.headers[

            "X-XSS-Protection"

        ] = "1; mode=block"

        response.headers[

            "Referrer-Policy"

        ] = "strict-origin-when-cross-origin"

        response.headers[

            "Permissions-Policy"

        ] = "camera=(), microphone=(), geolocation=()"

        response.headers[

            "Server"

        ] = "PDF Master AI"

        return response

# ----------------------------------------------------------
# REGISTER
# ----------------------------------------------------------

def register_security(

    app: FastAPI

):

    app.add_middleware(

        SecurityMiddleware

    )