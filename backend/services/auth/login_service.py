# ==========================================================
# PDF MASTER AI
# Login Service
# ==========================================================

# ----------------------------------------------------------
# IMPORT
# ----------------------------------------------------------

from sqlalchemy.orm import Session

from models.user import User

from schemas.auth import LoginRequest

from repositories.user_repository import UserRepository

from core.password import verify_password

from core.jwt import (
    create_access_token,
    create_refresh_token
)

from core.logger import info

from exceptions.auth import (
    InvalidCredentialsException,
    AccountDisabledException
)


# ----------------------------------------------------------
# LOGIN SERVICE
# ----------------------------------------------------------

class LoginService:

    """
    User Login Service.
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
        email: str
    ) -> User | None:

        return self.repository.get_by_email(
            email
        )

    # ------------------------------------------------------
    # VERIFY USER
    # ------------------------------------------------------

    def verify_user(
        self,
        user: User,
        password: str
    ) -> None:

        if not verify_password(
            password,
            user.password_hash
        ):

            raise InvalidCredentialsException()

        if not user.is_active:

            raise AccountDisabledException()

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
        data: LoginRequest
    ) -> dict:

        user = self.get_user(
            data.email
        )

        if user is None:

            raise InvalidCredentialsException()

        self.verify_user(
            user,
            data.password
        )

        tokens = self.generate_tokens(
            user
        )

        info(
            f"User login: {user.email}"
        )

        return tokens