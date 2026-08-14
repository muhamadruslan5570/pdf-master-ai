# ==========================================================
# PDF MASTER AI
# User Service
# ==========================================================

# ----------------------------------------------------------
# IMPORT
# ----------------------------------------------------------

from sqlalchemy.orm import Session

from models.user import User

from repositories.user_repository import UserRepository

from schemas.user import (
    UserCreate,
    UserUpdate
)

from core.password import hash_password

from core.logger import info

from exceptions.database import (
    RecordNotFoundException,
    DuplicateRecordException
)


# ----------------------------------------------------------
# USER SERVICE
# ----------------------------------------------------------

class UserService:

    """
    User Management Service.
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

    def get(
        self,
        user_id: int
    ) -> User:

        user = self.repository.get_by_id(
            user_id
        )

        if user is None:

            raise RecordNotFoundException(
                "User"
            )

        return user

    # ------------------------------------------------------
    # GET ALL
    # ------------------------------------------------------

    def get_all(
        self
    ) -> list[User]:

        return self.repository.get_all()

    # ------------------------------------------------------
    # CREATE
    # ------------------------------------------------------

    def create(
        self,
        data: UserCreate
    ) -> User:

        if self.repository.email_exists(
            data.email
        ):

            raise DuplicateRecordException(
                "Email"
            )

        if self.repository.username_exists(
            data.username
        ):

            raise DuplicateRecordException(
                "Username"
            )

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

        user = self.repository.create(
            user
        )

        info(
            f"User created: {user.email}"
        )

        return user

    # ------------------------------------------------------
    # UPDATE
    # ------------------------------------------------------

    def update(
        self,
        user_id: int,
        data: UserUpdate
    ) -> User:

        user = self.get(
            user_id
        )

        update_data = data.model_dump(
            exclude_unset=True,
            exclude_none=True
        )

        allowed_fields = {
            "full_name",
            "username",
            "email",
            "role",
            "is_active",
            "is_verified",
            "is_admin",
            "profile_image"
        }

        for field, value in update_data.items():

            if field == "password":

                user.password_hash = hash_password(
                    value
                )

            elif field in allowed_fields:

                setattr(
                    user,
                    field,
                    value
                )

        user = self.repository.update(
            user
        )

        info(
            f"User updated: {user.email}"
        )

        return user

    # ------------------------------------------------------
    # DELETE
    # ------------------------------------------------------

    def delete(
        self,
        user_id: int
    ) -> None:

        user = self.get(
            user_id
        )

        self.repository.delete(
            user
        )

        info(
            f"User deleted: {user.email}"
        )

    # ------------------------------------------------------
    # ACTIVATE
    # ------------------------------------------------------

    def activate(
        self,
        user_id: int
    ) -> User:

        user = self.get(
            user_id
        )

        return self.repository.activate(
            user
        )

    # ------------------------------------------------------
    # DEACTIVATE
    # ------------------------------------------------------

    def deactivate(
        self,
        user_id: int
    ) -> User:

        user = self.get(
            user_id
        )

        return self.repository.deactivate(
            user
        )