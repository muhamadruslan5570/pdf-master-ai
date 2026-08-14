# ==========================================================
# PDF MASTER AI
# Forgot Password Service
# ==========================================================

# ----------------------------------------------------------
# IMPORT
# ----------------------------------------------------------

import hashlib

from datetime import (
    datetime,
    timedelta
)

from sqlalchemy.orm import Session

from models.user import User

from models.password_reset_token import (
    PasswordResetToken
)

from schemas.auth import (
    ForgotPasswordRequest
)

from repositories.user_repository import (
    UserRepository
)

from repositories.password_reset_token_repository import (
    PasswordResetTokenRepository
)

from core.jwt import (
    create_reset_password_token
)

from core.config import (
    FRONTEND_URL
)

from core.logger import info

from services.email.email_service import (
    EmailService
)

from exceptions.database import (
    RecordNotFoundException
)


# ----------------------------------------------------------
# FORGOT PASSWORD SERVICE
# ----------------------------------------------------------

class ForgotPasswordService:

    """
    Forgot Password Service.
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

        self.email_service = EmailService()


    # ------------------------------------------------------
    # GET USER
    # ------------------------------------------------------

    def get_user(
        self,
        email: str
    ) -> User | None:

        return self.repository.get_by_email(
            email
        )


    # ------------------------------------------------------
    # GENERATE TOKEN
    # ------------------------------------------------------

    def generate_token(
        self,
        user: User
    ) -> str:

        return create_reset_password_token(
            {
                "user_id": user.id,
                "email": user.email
            }
        )


    # ------------------------------------------------------
    # HASH TOKEN
    # ------------------------------------------------------

    def hash_token(
        self,
        token: str
    ) -> str:

        return hashlib.sha256(
            token.encode("utf-8")
        ).hexdigest()


    # ------------------------------------------------------
    # SAVE RESET TOKEN
    # ------------------------------------------------------

    def save_reset_token(
        self,
        user: User,
        token: str
    ) -> PasswordResetToken:

        # --------------------------------------------------
        # DELETE OLD TOKENS
        # --------------------------------------------------

        self.token_repository.delete_user_tokens(
            user.id
        )


        # --------------------------------------------------
        # HASH TOKEN
        # --------------------------------------------------

        token_hash = self.hash_token(
            token
        )


        # --------------------------------------------------
        # EXPIRATION
        # --------------------------------------------------

        expires_at = (
            datetime.utcnow()
            + timedelta(
                minutes=30
            )
        )


        # --------------------------------------------------
        # CREATE TOKEN RECORD
        # --------------------------------------------------

        reset_token = PasswordResetToken(

            user_id=user.id,

            token_hash=token_hash,

            expires_at=expires_at,

            used_at=None

        )


        # --------------------------------------------------
        # SAVE TOKEN
        # --------------------------------------------------

        return self.token_repository.create(
            reset_token
        )


    # ------------------------------------------------------
    # CREATE RESET URL
    # ------------------------------------------------------

    def create_reset_url(
        self,
        token: str
    ) -> str:

        frontend_url = (
            FRONTEND_URL.rstrip("/")
        )

        return (
            f"{frontend_url}"
            f"/reset-password.html"
            f"?token={token}"
        )


    # ------------------------------------------------------
    # SEND RESET EMAIL
    # ------------------------------------------------------

    def send_reset_email(
        self,
        user: User,
        token: str
    ) -> None:

        reset_url = self.create_reset_url(
            token
        )

        self.email_service.send_password_reset_email(
            to_email=user.email,
            reset_url=reset_url
        )


    # ------------------------------------------------------
    # EXECUTE
    # ------------------------------------------------------

    def execute(
        self,
        data: ForgotPasswordRequest
    ) -> dict:

        # --------------------------------------------------
        # GET USER
        # --------------------------------------------------

        user = self.get_user(
            data.email
        )


        if user is None:

            raise RecordNotFoundException(
                "User"
            )


        # --------------------------------------------------
        # GENERATE TOKEN
        # --------------------------------------------------

        token = self.generate_token(
            user
        )


        # --------------------------------------------------
        # SAVE TOKEN
        # --------------------------------------------------

        self.save_reset_token(
            user,
            token
        )


        # --------------------------------------------------
        # SEND EMAIL
        # --------------------------------------------------

        self.send_reset_email(
            user,
            token
        )


        # --------------------------------------------------
        # LOG
        # --------------------------------------------------

        info(
            f"Password reset email sent: {user.email}"
        )


        # --------------------------------------------------
        # RESPONSE
        # --------------------------------------------------

        return {

            "success": True,

            "message": (
                "Password reset instructions "
                "have been sent to your email."
            )

        }