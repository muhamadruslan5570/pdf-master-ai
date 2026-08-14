# ==========================================================
# PDF MASTER AI
# Authentication Schemas
# ==========================================================

# ----------------------------------------------------------
# IMPORT
# ----------------------------------------------------------

from pydantic import (
    EmailStr,
    Field
)

from schemas.base import BaseSchema


# ----------------------------------------------------------
# LOGIN REQUEST
# ----------------------------------------------------------

class LoginRequest(BaseSchema):

    email: EmailStr

    password: str = Field(
        min_length=8,
        max_length=100
    )


# ----------------------------------------------------------
# REGISTER REQUEST
# ----------------------------------------------------------

class RegisterRequest(BaseSchema):

    full_name: str = Field(
        min_length=3,
        max_length=150
    )

    username: str = Field(
        min_length=3,
        max_length=100
    )

    email: EmailStr

    password: str = Field(
        min_length=8,
        max_length=100
    )


# ----------------------------------------------------------
# TOKEN RESPONSE
# ----------------------------------------------------------

class TokenResponse(BaseSchema):

    access_token: str

    refresh_token: str

    token_type: str = "Bearer"


# ----------------------------------------------------------
# REFRESH TOKEN
# ----------------------------------------------------------

class RefreshTokenRequest(BaseSchema):

    refresh_token: str


# ----------------------------------------------------------
# CHANGE PASSWORD
# ----------------------------------------------------------

class ChangePasswordRequest(BaseSchema):

    current_password: str

    new_password: str = Field(
        min_length=8,
        max_length=100
    )


# ----------------------------------------------------------
# FORGOT PASSWORD
# ----------------------------------------------------------

class ForgotPasswordRequest(BaseSchema):

    email: EmailStr


# ----------------------------------------------------------
# RESET PASSWORD
# ----------------------------------------------------------

class ResetPasswordRequest(BaseSchema):

    token: str

    new_password: str = Field(
        min_length=8,
        max_length=100
    )


# ----------------------------------------------------------
# VERIFY EMAIL
# ----------------------------------------------------------

class VerifyEmailRequest(BaseSchema):

    token: str