# ==========================================================
# PDF MASTER AI
# Authentication Exceptions
# ==========================================================

# ----------------------------------------------------------
# IMPORT
# ----------------------------------------------------------

from fastapi import (
    HTTPException,
    status
)

# ----------------------------------------------------------
# INVALID CREDENTIALS
# ----------------------------------------------------------

class InvalidCredentialsException(

    HTTPException

):

    def __init__(self):

        super().__init__(

            status_code=status.HTTP_401_UNAUTHORIZED,

            detail="Invalid email or password."

        )

# ----------------------------------------------------------
# INVALID TOKEN
# ----------------------------------------------------------

class InvalidTokenException(

    HTTPException

):

    def __init__(self):

        super().__init__(

            status_code=status.HTTP_401_UNAUTHORIZED,

            detail="Invalid or expired token."

        )

# ----------------------------------------------------------
# TOKEN EXPIRED
# ----------------------------------------------------------

class TokenExpiredException(

    HTTPException

):

    def __init__(self):

        super().__init__(

            status_code=status.HTTP_401_UNAUTHORIZED,

            detail="Token has expired."

        )

# ----------------------------------------------------------
# EMAIL NOT VERIFIED
# ----------------------------------------------------------

class EmailNotVerifiedException(

    HTTPException

):

    def __init__(self):

        super().__init__(

            status_code=status.HTTP_403_FORBIDDEN,

            detail="Email has not been verified."

        )

# ----------------------------------------------------------
# ACCOUNT DISABLED
# ----------------------------------------------------------

class AccountDisabledException(

    HTTPException

):

    def __init__(self):

        super().__init__(

            status_code=status.HTTP_403_FORBIDDEN,

            detail="Account has been disabled."

        )

# ----------------------------------------------------------
# ACCOUNT LOCKED
# ----------------------------------------------------------

class AccountLockedException(

    HTTPException

):

    def __init__(self):

        super().__init__(

            status_code=status.HTTP_423_LOCKED,

            detail="Account has been locked."

        )

# ----------------------------------------------------------
# UNAUTHORIZED
# ----------------------------------------------------------

class UnauthorizedException(

    HTTPException

):

    def __init__(self):

        super().__init__(

            status_code=status.HTTP_401_UNAUTHORIZED,

            detail="Unauthorized."

        )

# ----------------------------------------------------------
# FORBIDDEN
# ----------------------------------------------------------

class ForbiddenException(

    HTTPException

):

    def __init__(self):

        super().__init__(

            status_code=status.HTTP_403_FORBIDDEN,

            detail="Access denied."

        )