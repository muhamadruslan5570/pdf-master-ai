# ==========================================================
# PDF MASTER AI
# Authentication API
# ==========================================================

# ----------------------------------------------------------
# IMPORT
# ----------------------------------------------------------

from fastapi import (
    APIRouter,
    Depends,
    status
)

from fastapi.security import OAuth2PasswordRequestForm

from sqlalchemy.orm import Session

from dependencies.database import get_db

from schemas.auth import (
    LoginRequest,
    RegisterRequest,
    RefreshTokenRequest,
    ForgotPasswordRequest,
    ResetPasswordRequest,
    VerifyEmailRequest
)

from services.auth.register_service import RegisterService
from services.auth.login_service import LoginService
from services.auth.refresh_token_service import RefreshTokenService
from services.auth.forgot_password_service import ForgotPasswordService
from services.auth.reset_password_service import ResetPasswordService
from services.auth.verify_email_service import VerifyEmailService


# ----------------------------------------------------------
# ROUTER
# ----------------------------------------------------------

router = APIRouter()


# ==========================================================
# REGISTER
# ==========================================================

@router.post(
    "/register",
    status_code=status.HTTP_201_CREATED,
    summary="Register User"
)
def register(
    data: RegisterRequest,
    db: Session = Depends(get_db)
):

    service = RegisterService(db)

    user, verification_token = service.execute(
        data
    )

    return {
        "success": True,
        "message": "User registered successfully.",
        "user": {
            "id": user.id,
            "full_name": user.full_name,
            "username": user.username,
            "email": user.email,
            "role": user.role,
            "is_active": user.is_active,
            "is_verified": user.is_verified
        },
        "verification_token": verification_token
    }


# ==========================================================
# LOGIN
# ==========================================================

@router.post(
    "/login",
    summary="Login User"
)
def login(
    data: LoginRequest,
    db: Session = Depends(get_db)
):

    service = LoginService(db)

    tokens = service.execute(
        data
    )

    return {
        "success": True,
        "message": "Login successful.",
        **tokens
    }


# ==========================================================
# REFRESH TOKEN
# ==========================================================

@router.post(
    "/refresh",
    summary="Refresh Access Token"
)
def refresh_token(
    data: RefreshTokenRequest,
    db: Session = Depends(get_db)
):

    service = RefreshTokenService(db)

    tokens = service.execute(
        data
    )

    return {
        "success": True,
        "message": "Token refreshed successfully.",
        **tokens
    }


# ==========================================================
# FORGOT PASSWORD
# ==========================================================

@router.post(
    "/forgot-password",
    summary="Forgot Password"
)
def forgot_password(
    data: ForgotPasswordRequest,
    db: Session = Depends(get_db)
):

    service = ForgotPasswordService(db)

    result = service.execute(
        data
    )

    return {
        "success": True,
        "message": "Password reset token generated.",
        **result
    }


# ==========================================================
# RESET PASSWORD
# ==========================================================

@router.post(
    "/reset-password",
    summary="Reset Password"
)
def reset_password(
    data: ResetPasswordRequest,
    db: Session = Depends(get_db)
):

    service = ResetPasswordService(db)

    user = service.execute(
        data
    )

    return {
        "success": True,
        "message": "Password reset successfully.",
        "user": {
            "id": user.id,
            "email": user.email
        }
    }


# ==========================================================
# VERIFY EMAIL
# ==========================================================

@router.post(
    "/verify-email",
    summary="Verify Email"
)
def verify_email(
    data: VerifyEmailRequest,
    db: Session = Depends(get_db)
):

    service = VerifyEmailService(db)

    user = service.execute(
        data
    )

    return {
        "success": True,
        "message": "Email verified successfully.",
        "user": {
            "id": user.id,
            "email": user.email,
            "is_verified": user.is_verified
        }
    }

# ==========================================================
# OAUTH2 LOGIN
# ==========================================================

@router.post(
    "/token",
    summary="OAuth2 Login"
)
def oauth2_login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):

    data = LoginRequest(
        email=form_data.username,
        password=form_data.password
    )

    service = LoginService(
        db
    )

    tokens = service.execute(
        data
    )

    return {
        "access_token": tokens["access_token"],
        "refresh_token": tokens["refresh_token"],
        "token_type": "bearer"
    }


# ==========================================================
# END
# ==========================================================