# ==========================================================
# PDF MASTER AI
# CORS Middleware
# ==========================================================

# ----------------------------------------------------------
# IMPORT
# ----------------------------------------------------------

from fastapi import FastAPI

from fastapi.middleware.cors import CORSMiddleware


# ----------------------------------------------------------
# ALLOWED ORIGINS
# ----------------------------------------------------------

ALLOWED_ORIGINS = [

    # ------------------------------------------------------
    # LOCAL DEVELOPMENT
    # ------------------------------------------------------

    "http://localhost",
    "http://localhost:3000",
    "http://localhost:5500",

    "http://127.0.0.1",
    "http://127.0.0.1:3000",
    "http://127.0.0.1:5500",

    # ------------------------------------------------------
    # HTTPS LOCAL
    # ------------------------------------------------------

    "https://localhost",
    "https://localhost:5500",

    "https://127.0.0.1",
    "https://127.0.0.1:5500",

    # ------------------------------------------------------
    # PRODUCTION
    # ------------------------------------------------------
    #
    # Nanti masukkan domain frontend asli di sini.
    #
    # Contoh:
    #
    # "https://pdfmasterai.com",
    # "https://www.pdfmasterai.com",
    #
    # Cloudflare Pages:
    #
    # "https://pdf-master-ai.pages.dev",
    #
    # ------------------------------------------------------

]


# ----------------------------------------------------------
# REGISTER CORS
# ----------------------------------------------------------

def register_cors(
    app: FastAPI
) -> None:

    """
    Register CORS Middleware.
    """

    app.add_middleware(

        CORSMiddleware,

        allow_origins=ALLOWED_ORIGINS,

        allow_credentials=True,

        allow_methods=[
            "*"
        ],

        allow_headers=[
            "*"
        ],

        expose_headers=[
            "*"
        ]

    )