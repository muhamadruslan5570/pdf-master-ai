# ==========================================================
# PDF MASTER AI
# Health API
# ==========================================================

# ----------------------------------------------------------
# IMPORT
# ----------------------------------------------------------

from datetime import datetime

from fastapi import APIRouter

# ----------------------------------------------------------
# ROUTER
# ----------------------------------------------------------

router = APIRouter()

# ----------------------------------------------------------
# HEALTH CHECK
# ----------------------------------------------------------

@router.get(
    "/",
    summary="Health Check"
)
async def health():

    return {

        "success": True,

        "message": "PDF Master AI API is running.",

        "status": "healthy",

        "version": "1.0.0",

        "timestamp": datetime.utcnow().isoformat()

    }

# ----------------------------------------------------------
# PING
# ----------------------------------------------------------

@router.get(
    "/ping",
    summary="Ping API"
)
async def ping():

    return {

        "success": True,

        "message": "Pong"

    }

# ----------------------------------------------------------
# VERSION
# ----------------------------------------------------------

@router.get(
    "/version",
    summary="API Version"
)
async def version():

    return {

        "application": "PDF Master AI",

        "version": "1.0.0"

    }