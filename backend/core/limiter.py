# ==========================================================
# PDF MASTER AI
# Rate Limiter
# ==========================================================

# ----------------------------------------------------------
# IMPORT
# ----------------------------------------------------------

from slowapi import Limiter
from slowapi.util import get_remote_address

# ----------------------------------------------------------
# LIMITER
# ----------------------------------------------------------

limiter = Limiter(

    key_func=get_remote_address,

    default_limits=[

        "1000/hour"

    ]

)

# ----------------------------------------------------------
# AUTH LIMITS
# ----------------------------------------------------------

LOGIN_LIMIT = "5/minute"

REGISTER_LIMIT = "3/10minutes"

FORGOT_PASSWORD_LIMIT = "3/30minutes"

RESET_PASSWORD_LIMIT = "5/30minutes"

VERIFY_EMAIL_LIMIT = "10/hour"

# ----------------------------------------------------------
# USER LIMITS
# ----------------------------------------------------------

PROFILE_UPDATE_LIMIT = "20/hour"

CHANGE_PASSWORD_LIMIT = "5/hour"

# ----------------------------------------------------------
# FILE LIMITS
# ----------------------------------------------------------

UPLOAD_LIMIT = "50/hour"

DOWNLOAD_LIMIT = "500/hour"

DELETE_FILE_LIMIT = "100/hour"

# ----------------------------------------------------------
# PDF LIMITS
# ----------------------------------------------------------

COMPRESS_PDF_LIMIT = "100/hour"

MERGE_PDF_LIMIT = "100/hour"

SPLIT_PDF_LIMIT = "100/hour"

ROTATE_PDF_LIMIT = "100/hour"

OCR_LIMIT = "30/hour"

# ----------------------------------------------------------
# IMAGE LIMITS
# ----------------------------------------------------------

COMPRESS_IMAGE_LIMIT = "100/hour"

REMOVE_BACKGROUND_LIMIT = "30/hour"

UPSCALER_LIMIT = "30/hour"

IMAGE_TO_TEXT_LIMIT = "50/hour"

# ----------------------------------------------------------
# AI LIMITS
# ----------------------------------------------------------

CHAT_PDF_LIMIT = "50/hour"

SUMMARIZE_LIMIT = "50/hour"

TRANSLATE_LIMIT = "50/hour"

AI_WRITER_LIMIT = "30/hour"

# ----------------------------------------------------------
# API LIMITS
# ----------------------------------------------------------

FREE_API_LIMIT = "100/day"

PREMIUM_API_LIMIT = "10000/day"

# ----------------------------------------------------------
# ADMIN
# ----------------------------------------------------------

ADMIN_LIMIT = "unlimited"