# ==========================================================
# PDF MASTER AI
# Main API Router
# ==========================================================

# ----------------------------------------------------------
# IMPORT
# ----------------------------------------------------------

from fastapi import APIRouter

from api.v1.health import router as health_router
from api.v1.pdf import router as pdf_router
from api.v1.storage import router as storage_router
from api.v1.auth import router as auth_router
from api.v1.users import router as users_router
from api.v1.history import router as history_router
from api.v1.image import router as image_router


# ----------------------------------------------------------
# API ROUTER
# ----------------------------------------------------------

api_router = APIRouter()


# ==========================================================
# HEALTH
# ==========================================================

api_router.include_router(
    health_router,
    prefix="/health",
    tags=["Health"]
)


# ==========================================================
# AUTHENTICATION
# ==========================================================

api_router.include_router(
    auth_router,
    prefix="/auth",
    tags=["Authentication"]
)


# ==========================================================
# USERS
# ==========================================================

api_router.include_router(
    users_router,
    prefix="/users",
    tags=["Users"]
)


# ==========================================================
# PDF
# ==========================================================

api_router.include_router(
    pdf_router,
    prefix="/pdf",
    tags=["PDF"]
)


# ==========================================================
# STORAGE
# ==========================================================

api_router.include_router(
    storage_router,
    prefix="/storage",
    tags=["Storage"]
)


# ==========================================================

# ==========================================================
# HISTORY
# ==========================================================

api_router.include_router(
    history_router,
    prefix="/history",
    tags=["History"]
)

# ==========================================================
# IMAGE
# ==========================================================

api_router.include_router(
    image_router,
    prefix="/image",
    tags=["Image"]
)
# END
# ==========================================================



