# ==========================================================
# PDF MASTER AI
# Current User Dependency
# ==========================================================

# ----------------------------------------------------------
# IMPORT
# ----------------------------------------------------------

from fastapi import (
    Depends,
    HTTPException,
    status
)

from sqlalchemy.orm import Session

from core.jwt import verify_token

from dependencies.auth import get_token

from dependencies.database import get_db

from models.user import User

from repositories.user_repository import UserRepository


# ----------------------------------------------------------
# CURRENT USER
# ----------------------------------------------------------

def get_current_user(
    token: str = Depends(get_token),
    db: Session = Depends(get_db)
) -> User:

    """
    Get current authenticated user.
    """

    payload = verify_token(
        token
    )

    if payload is None:

        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token"
        )

    user_id = payload.get(
        "user_id"
    )

    if user_id is None:

        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token payload"
        )

    repository = UserRepository(
        db
    )

    user = repository.get_by_id(
        user_id
    )

    if user is None:

        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    if not user.is_active:

        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User account is inactive"
        )

    return user


# ----------------------------------------------------------
# CURRENT ACTIVE USER
# ----------------------------------------------------------

def get_current_active_user(
    current_user: User = Depends(
        get_current_user
    )
) -> User:

    """
    Get active user.
    """

    return current_user


# ----------------------------------------------------------
# CURRENT VERIFIED USER
# ----------------------------------------------------------

def get_current_verified_user(
    current_user: User = Depends(
        get_current_user
    )
) -> User:

    """
    Get verified user.
    """

    if not current_user.is_verified:

        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Email not verified"
        )

    return current_user