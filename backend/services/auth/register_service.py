# ==========================================================
# PDF MASTER AI
# Register Service
# ==========================================================

# ----------------------------------------------------------
# IMPORT
# ----------------------------------------------------------

from sqlalchemy.orm import Session

from models.user import User

from schemas.auth import RegisterRequest

from repositories.user_repository import UserRepository

from core.password import hash_password

from core.jwt import create_verify_email_token

from core.logger import info

from exceptions.database import (
    DuplicateRecordException
)

# ----------------------------------------------------------
# REGISTER SERVICE
# ----------------------------------------------------------

class RegisterService:

    """
    User Registration Service.
    """

    def __init__(
        self,
        db: Session
    ):

        self.repository = UserRepository(
            db
        )

    # ------------------------------------------------------
    # CHECK EMAIL
    # ------------------------------------------------------

    def email_exists(
        self,
        email: str
    ) -> bool:

        return self.repository.email_exists(
            email
        )

    # ------------------------------------------------------
    # CHECK USERNAME
    # ------------------------------------------------------

    def username_exists(
        self,
        username: str
    ) -> bool:

        return self.repository.username_exists(
            username
        )

    # ------------------------------------------------------
    # CREATE USER
    # ------------------------------------------------------

    def create_user(
        self,
        data: RegisterRequest
    ) -> User:

        user = User(
            full_name=data.full_name,
            username=data.username,
            email=data.email,
            password_hash=hash_password(
                data.password
            ),
            role="user",
            is_active=True,
            is_verified=False,
            is_admin=False
        )

        return self.repository.create(
            user
        )

    # ------------------------------------------------------
    # CREATE VERIFICATION TOKEN
    # ------------------------------------------------------

    def create_verification_token(
        self,
        user: User
    ) -> str:

        return create_verify_email_token({
            "user_id": user.id
        })

    # ------------------------------------------------------
    # EXECUTE
    # ------------------------------------------------------

    def execute(
        self,
        data: RegisterRequest
    ) -> tuple[User, str]:

        """
        Register new user and generate
        email verification token.
        """

        if self.email_exists(
            data.email
        ):

            raise DuplicateRecordException(
                "Email"
            )

        if self.username_exists(
            data.username
        ):

            raise DuplicateRecordException(
                "Username"
            )

        user = self.create_user(
            data
        )

        verification_token = (
            self.create_verification_token(
                user
            )
        )

        info(
            f"New user registered: {user.email}"
        )

        return (
            user,
            verification_token
        )


# ==========================================================
# END
# ==========================================================