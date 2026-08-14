# ==========================================================
# PDF MASTER AI
# Refresh Token Service
# ==========================================================

# ----------------------------------------------------------
# IMPORT
# ----------------------------------------------------------

from sqlalchemy.orm import Session

from models.user import User

from schemas.auth import RefreshTokenRequest

from repositories.user_repository import UserRepository

from core.jwt import (
    verify_token,
    create_access_token,
    create_refresh_token
)

from core.logger import info

from exceptions.auth import (
    InvalidTokenException,
    AccountDisabledException
)


# ----------------------------------------------------------
# REFRESH TOKEN SERVICE
# ----------------------------------------------------------

class RefreshTokenService:

    """
    Refresh JWT Token Service.
    """

    def __init__(
        self,
        db: Session
    ):

        self.repository = UserRepository(
            db
        )

    # ------------------------------------------------------
    # GET USER
    # ------------------------------------------------------

    def get_user(
        self,
        user_id: int
    ) -> User | None:

        return self.repository.get_by_id(
            user_id
        )

    # ------------------------------------------------------
    # VERIFY REFRESH TOKEN
    # ------------------------------------------------------

    def verify_refresh_token(
        self,
        refresh_token: str
    ) -> dict:

        payload = verify_token(
            refresh_token
        )

        if payload is None:

            raise InvalidTokenException()

        if payload.get(
            "type"
        ) != "refresh":

            raise InvalidTokenException()

        return payload

    # ------------------------------------------------------
    # GENERATE TOKEN
    # ------------------------------------------------------

    def generate_tokens(
        self,
        user: User
    ) -> dict:

        access_token = create_access_token(
            {
                "user_id": user.id,
                "email": user.email,
                "role": user.role
            }
        )

        refresh_token = create_refresh_token(
            {
                "user_id": user.id
            }
        )

        return {
            "access_token": access_token,
            "refresh_token": refresh_token,
            "token_type": "bearer"
        }

    # ------------------------------------------------------
    # EXECUTE
    # ------------------------------------------------------

    def execute(
        self,
        data: RefreshTokenRequest
    ) -> dict:

        payload = self.verify_refresh_token(
            data.refresh_token
        )

        user = self.get_user(
            payload["user_id"]
        )

        if user is None:

            raise InvalidTokenException()

        if not user.is_active:

            raise AccountDisabledException()

        tokens = self.generate_tokens(
            user
        )

        info(
            f"Refresh token: {user.email}"
        )

        return tokens