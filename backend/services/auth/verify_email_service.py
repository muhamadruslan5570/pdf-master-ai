# ==========================================================
# PDF MASTER AI
# Verify Email Service
# ==========================================================

# ----------------------------------------------------------
# IMPORT
# ----------------------------------------------------------

from sqlalchemy.orm import Session

from models.user import User

from schemas.auth import VerifyEmailRequest

from repositories.user_repository import UserRepository

from core.jwt import verify_token

from core.logger import info

from exceptions.auth import (
    InvalidTokenException,
    EmailNotVerifiedException
)


# ----------------------------------------------------------
# VERIFY EMAIL SERVICE
# ----------------------------------------------------------

class VerifyEmailService:

    """
    Verify User Email Service.
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
    # VERIFY TOKEN
    # ------------------------------------------------------

    def verify_email_token(
        self,
        token: str
    ) -> dict:

        payload = verify_token(
            token
        )

        if payload is None:

            raise InvalidTokenException()

        if payload.get(
            "type"
        ) != "verify_email":

            raise InvalidTokenException()

        return payload

    # ------------------------------------------------------
    # ACTIVATE USER
    # ------------------------------------------------------

    def activate_user(
        self,
        user: User
    ) -> User:

        user.is_verified = True

        return self.repository.update(
            user
        )

    # ------------------------------------------------------
    # EXECUTE
    # ------------------------------------------------------

    def execute(
        self,
        data: VerifyEmailRequest
    ) -> User:

        payload = self.verify_email_token(
            data.token
        )

        user = self.get_user(
            payload["user_id"]
        )

        if user is None:

            raise InvalidTokenException()

        if user.is_verified:

            return user

        user = self.activate_user(
            user
        )

        info(
            f"Email verified: {user.email}"
        )

        return user