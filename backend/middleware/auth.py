# ==========================================================
# PDF MASTER AI
# Authentication Middleware
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

from core.jwt import verify_token

# ----------------------------------------------------------
# AUTH MIDDLEWARE
# ----------------------------------------------------------

class AuthenticationMiddleware(
    BaseHTTPMiddleware
):

    async def dispatch(
        self,
        request: Request,
        call_next
    ):

        request.state.user = None

        authorization = request.headers.get(
            "Authorization"
        )

        if authorization:

            if authorization.startswith(
                "Bearer "
            ):

                token = authorization.replace(
                    "Bearer ",
                    ""
                ).strip()

                payload = verify_token(
                    token
                )

                if payload:

                    request.state.user = payload

        response = await call_next(
            request
        )

        return response

# ----------------------------------------------------------
# REGISTER
# ----------------------------------------------------------

def register_auth(
    app: FastAPI
) -> None:
    """
    Register Authentication Middleware.
    """

    app.add_middleware(
        AuthenticationMiddleware
    )