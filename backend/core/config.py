# ==========================================================
# PDF MASTER AI
# Configuration
# ==========================================================

# ----------------------------------------------------------
# IMPORT
# ----------------------------------------------------------

import os

from dotenv import load_dotenv


# ----------------------------------------------------------
# LOAD ENVIRONMENT
# ----------------------------------------------------------

load_dotenv()


# ----------------------------------------------------------
# APPLICATION
# ----------------------------------------------------------

APP_NAME = os.getenv(
    "APP_NAME",
    "PDF Master AI"
)

APP_VERSION = os.getenv(
    "APP_VERSION",
    "1.0.0"
)

DEBUG = os.getenv(
    "DEBUG",
    "False"
).lower() == "true"


# ----------------------------------------------------------
# SERVER
# ----------------------------------------------------------

HOST = os.getenv(
    "HOST",
    "0.0.0.0"
)

PORT = int(
    os.getenv(
        "PORT",
        "8000"
    )
)


# ----------------------------------------------------------
# DOMAIN
# ----------------------------------------------------------

FRONTEND_URL = os.getenv(
    "FRONTEND_URL",
    "http://localhost:5500"
)

API_URL = os.getenv(
    "API_URL",
    "http://localhost:8000"
)


# ----------------------------------------------------------
# DATABASE
# ----------------------------------------------------------

DATABASE_URL = os.getenv(
    "DATABASE_URL"
)


# ----------------------------------------------------------
# JWT
# ----------------------------------------------------------

SECRET_KEY = os.getenv(
    "SECRET_KEY"
)

ALGORITHM = os.getenv(
    "ALGORITHM",
    "HS256"
)

ACCESS_TOKEN_EXPIRE_MINUTES = int(
    os.getenv(
        "ACCESS_TOKEN_EXPIRE_MINUTES",
        "30"
    )
)

REFRESH_TOKEN_EXPIRE_DAYS = int(
    os.getenv(
        "REFRESH_TOKEN_EXPIRE_DAYS",
        "7"
    )
)


# ----------------------------------------------------------
# GEMINI
# ----------------------------------------------------------

GEMINI_API_KEY = os.getenv(
    "GEMINI_API_KEY"
)


# ----------------------------------------------------------
# STORAGE
# ----------------------------------------------------------

R2_ACCOUNT_ID = os.getenv(
    "R2_ACCOUNT_ID"
)

R2_ACCESS_KEY = os.getenv(
    "R2_ACCESS_KEY"
)

R2_SECRET_KEY = os.getenv(
    "R2_SECRET_KEY"
)

R2_BUCKET = os.getenv(
    "R2_BUCKET"
)


# ----------------------------------------------------------
# EMAIL
# ----------------------------------------------------------

SMTP_SERVER = os.getenv(
    "SMTP_SERVER"
)

SMTP_PORT = os.getenv(
    "SMTP_PORT",
    "587"
)

SMTP_USERNAME = os.getenv(
    "SMTP_USERNAME"
)

SMTP_PASSWORD = os.getenv(
    "SMTP_PASSWORD"
)


# ----------------------------------------------------------
# PAYMENT
# ----------------------------------------------------------

MIDTRANS_SERVER_KEY = os.getenv(
    "MIDTRANS_SERVER_KEY"
)

XENDIT_SECRET_KEY = os.getenv(
    "XENDIT_SECRET_KEY"
)