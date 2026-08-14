# ==========================================================
# PDF MASTER AI
# Trusted Hosts Middleware
# ==========================================================

# ----------------------------------------------------------
# IMPORT
# ----------------------------------------------------------

from fastapi import FastAPI

from starlette.middleware.trustedhost import (

    TrustedHostMiddleware

)

# ----------------------------------------------------------
# TRUSTED HOSTS
# ----------------------------------------------------------

TRUSTED_HOSTS = [

    "localhost",

    "127.0.0.1",

    "*.localhost",

    "*.onrender.com",

    "*.pages.dev",

    "*.my.id",

    "*.com"

]

# ----------------------------------------------------------
# REGISTER
# ----------------------------------------------------------

def register_trusted_hosts(

    app: FastAPI

) -> None:
    """
    Register Trusted Hosts Middleware.
    """

    app.add_middleware(

        TrustedHostMiddleware,

        allowed_hosts=TRUSTED_HOSTS

    )