# ==========================================================
# PDF MASTER AI
# API Dependencies
# ==========================================================

# ----------------------------------------------------------
# IMPORT
# ----------------------------------------------------------

from typing import Generator

from fastapi import Depends
from fastapi import HTTPException
from fastapi import status

from fastapi.security import OAuth2PasswordBearer

from sqlalchemy.orm import Session

from database.session import SessionLocal

from dependencies.auth import get_current_user

from models.user import User

# ----------------------------------------------------------
# DATABASE
# ----------------------------------------------------------

def get_db() -> Generator[Session, None, None]:

    db = SessionLocal()

    try:

        yield db

    finally:

        db.close()

# ----------------------------------------------------------
# OAUTH2
# ----------------------------------------------------------

oauth2_scheme = OAuth2PasswordBearer(

    tokenUrl="/api/v1/auth/login"

)

# ----------------------------------------------------------
# CURRENT USER
# ----------------------------------------------------------

CurrentUser = Depends(

    get_current_user

)

# ----------------------------------------------------------
# CURRENT ACTIVE USER
# ----------------------------------------------------------

def get_current_active_user(

    current_user: User = Depends(

        get_current_user

    )

) -> User:

    if hasattr(current_user, "is_active"):

        if not current_user.is_active:

            raise HTTPException(

                status_code=status.HTTP_403_FORBIDDEN,

                detail="Inactive user."

            )

    return current_user

# ----------------------------------------------------------
# CURRENT SUPER USER
# ----------------------------------------------------------

def get_current_superuser(

    current_user: User = Depends(

        get_current_user

    )

) -> User:

    if hasattr(current_user, "is_superuser"):

        if not current_user.is_superuser:

            raise HTTPException(

                status_code=status.HTTP_403_FORBIDDEN,

                detail="Permission denied."

            )

    return current_user

# ----------------------------------------------------------
# DEPENDENCY SHORTCUTS
# ----------------------------------------------------------

CurrentActiveUser = Depends(

    get_current_active_user

)

CurrentSuperUser = Depends(

    get_current_superuser

)