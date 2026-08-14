# ==========================================================
# PDF MASTER AI
# Logging Middleware
# ==========================================================

# ----------------------------------------------------------
# IMPORT
# ----------------------------------------------------------

import time

from fastapi import (
    FastAPI,
    Request
)

from starlette.middleware.base import (
    BaseHTTPMiddleware
)

from core.logger import info

# ----------------------------------------------------------
# LOGGING MIDDLEWARE
# ----------------------------------------------------------

class LoggingMiddleware(
    BaseHTTPMiddleware
):

    async def dispatch(
        self,
        request: Request,
        call_next
    ):

        start_time = time.time()

        response = await call_next(request)

        process_time = round(

            (time.time() - start_time) * 1000,

            2

        )

        info(

            f"{request.client.host} | "

            f"{request.method} | "

            f"{request.url.path} | "

            f"{response.status_code} | "

            f"{process_time} ms"

        )

        response.headers[

            "X-Process-Time"

        ] = str(process_time)

        return response

# ----------------------------------------------------------
# REGISTER
# ----------------------------------------------------------

def register_logging(
    app: FastAPI
) -> None:

    app.add_middleware(
        LoggingMiddleware
    )