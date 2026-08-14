# ==========================================================
# PDF MASTER AI
# Reset Password Service
# ==========================================================

# ----------------------------------------------------------
# IMPORT
# ----------------------------------------------------------

import hashlib

from sqlalchemy.orm import Session

from models.user import User

from schemas.auth import ResetPasswordRequest

from repositories.user_repository import UserRepository

from repositories.password_reset_token_repository import (
    PasswordResetTokenRepository
)

from core.jwt import verify_token

from core.password import hash_password

from core.logger import info

from exceptions.auth import (
    InvalidTokenException,
    AccountDisabledException
)


# ----------------------------------------------------------
# RESET PASSWORD SERVICE
# ----------------------------------------------------------

class ResetPasswordService:

    """
    Reset Password Service.
    """

    def __init__(
        self,
        db: Session
    ):

        self.db = db

        self.repository = UserRepository(
            db
        )

        self.token_repository = (
            PasswordResetTokenRepository(
                db
            )
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
    # HASH RESET TOKEN
    # ------------------------------------------------------

    def hash_token(
        self,
        token: str
    ) -> str:

        return hashlib.sha256(
            token.encode("utf-8")
        ).hexdigest()


    # ------------------------------------------------------
    # VERIFY JWT
    # ------------------------------------------------------

    def verify_reset_token(
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
        ) != "reset_password":

            raise InvalidTokenException()


        if payload.get(
            "user_id"
        ) is None:

            raise InvalidTokenException()


        return payload


    # ------------------------------------------------------
    # VERIFY DATABASE TOKEN
    # ------------------------------------------------------

    def verify_database_token(
        self,
        token: str
    ):

        token_hash = self.hash_token(
            token
        )

        reset_token = (
            self.token_repository.get_valid_token(
                token_hash
            )
        )

        if reset_token is None:

            raise InvalidTokenException()


        return reset_token


    # ------------------------------------------------------
    # UPDATE PASSWORD
    # ------------------------------------------------------

    def update_password(
        self,
        user: User,
        password: str
    ) -> User:

        user.password_hash = hash_password(
            password
        )

        return self.repository.update(
            user
        )


    # ------------------------------------------------------
    # EXECUTE
    # ------------------------------------------------------

    def execute(
        self,
        data: ResetPasswordRequest
    ) -> User:

        # --------------------------------------------------
        # VERIFY JWT
        # --------------------------------------------------

        payload = self.verify_reset_token(
            data.token
        )


        # --------------------------------------------------
        # VERIFY DATABASE TOKEN
        # --------------------------------------------------

        reset_token = self.verify_database_token(
            data.token
        )


        # --------------------------------------------------
        # CHECK USER ID
        # --------------------------------------------------

        if (
            reset_token.user_id
            != payload["user_id"]
        ):

            raise InvalidTokenException()


        # --------------------------------------------------
        # GET USER
        # --------------------------------------------------

        user = self.get_user(
            payload["user_id"]
        )


        if user is None:

            raise InvalidTokenException()


        # --------------------------------------------------
        # CHECK ACCOUNT
        # --------------------------------------------------

        if not user.is_active:

            raise AccountDisabledException()


        # --------------------------------------------------
        # UPDATE PASSWORD
        # --------------------------------------------------

        user = self.update_password(
            user,
            data.new_password
        )


        # --------------------------------------------------
        # MARK TOKEN AS USED
        # --------------------------------------------------

        self.token_repository.mark_as_used(
            reset_token
        )


        # --------------------------------------------------
        # LOG
        # --------------------------------------------------

        info(
            f"Password changed: {user.email}"
        )


        return user