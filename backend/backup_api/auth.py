# ==========================================================
# PDF MASTER AI
# Authentication API
# ==========================================================

# ----------------------------------------------------------
# IMPORT
# ----------------------------------------------------------

from fastapi import APIRouter
from fastapi import Depends
from fastapi import status

from sqlalchemy.orm import Session

from api.deps import get_db
from api.deps import CurrentUser

from services.auth.auth_service import AuthService

from schemas.auth import (
    LoginRequest,
    RegisterRequest,
    TokenResponse
)

from schemas.user import (
    UserResponse
)

# ----------------------------------------------------------
# ROUTER
# ----------------------------------------------------------

router = APIRouter()

# ----------------------------------------------------------
# REGISTER
# ----------------------------------------------------------

@router.post(

    "/register",

    response_model=UserResponse,

    status_code=status.HTTP_201_CREATED,

    summary="Register User"

)
def register(

    request: RegisterRequest,

    db: Session = Depends(get_db)

):

    service = AuthService(db)

    return service.register(

        request

    )

# ----------------------------------------------------------
# LOGIN
# ----------------------------------------------------------

@router.post(

    "/login",

    response_model=TokenResponse,

    summary="Login"

)
def login(

    request: LoginRequest,

    db: Session = Depends(get_db)

):

    service = AuthService(db)

    return service.login(

        request

    )

# ----------------------------------------------------------
# PROFILE
# ----------------------------------------------------------

@router.get(

    "/me",

    response_model=UserResponse,

    summary="Current User"

)
def me(

    current_user = CurrentUser

):

    return current_user

# ----------------------------------------------------------
# REFRESH TOKEN
# ----------------------------------------------------------

@router.post(

    "/refresh",

    response_model=TokenResponse,

    summary="Refresh Token"

)
def refresh(

    current_user = CurrentUser,

    db: Session = Depends(get_db)

):

    service = AuthService(db)

    return service.refresh_token(

        current_user

    )

# ----------------------------------------------------------
# LOGOUT
# ----------------------------------------------------------

@router.post(

    "/logout",

    summary="Logout"

)
def logout(

    current_user = CurrentUser,

    db: Session = Depends(get_db)

):

    service = AuthService(db)

    service.logout(

        current_user

    )

    return {

        "success": True,

        "message": "Logout successful."

    }