# ==========================================================
# PDF MASTER AI
# Profile Service
# ==========================================================

# ----------------------------------------------------------
# IMPORT
# ----------------------------------------------------------

from sqlalchemy.orm import Session

from repositories.user_repository import UserRepository

from schemas.user import (

    ProfileUpdate,

    ChangePassword

)

from core.security import (

    hash_password,

    verify_password

)

from core.logger import info

from exceptions.database import (

    RecordNotFoundException

)

from exceptions.auth import (

    InvalidCredentialsException

)

# ----------------------------------------------------------
# PROFILE SERVICE
# ----------------------------------------------------------

class ProfileService:

    """
    User Profile Service.
    """

    def __init__(

        self,

        db: Session

    ):

        self.repository = UserRepository(

            db

        )

    # ------------------------------------------------------
    # GET PROFILE
    # ------------------------------------------------------

    def get_profile(

        self,

        user_id: int

    ):

        user = self.repository.get_by_id(

            user_id

        )

        if user is None:

            raise RecordNotFoundException(

                "User"

            )

        return user

    # ------------------------------------------------------
    # UPDATE PROFILE
    # ------------------------------------------------------

    def update_profile(

        self,

        user_id: int,

        data: ProfileUpdate

    ):

        user = self.get_profile(

            user_id

        )

        update_data = data.model_dump(

            exclude_none=True,

            exclude_unset=True

        )

       allowed_fields = {
    "full_name",
    "username",
    "email",
    "profile_image"
}

allowed_fields = {
    "full_name",
    "username",
    "email",
    "profile_image"
}

for field, value in update_data.items():

    if field in allowed_fields:

        setattr(
            user,
            field,
            value
        )        user = self.repository.update(

            user

        )

        info(

            f"Profile updated: {user.email}"

        )

        return user

    # ------------------------------------------------------
    # CHANGE PASSWORD
    # ------------------------------------------------------

    def change_password(

        self,

        user_id: int,

        data: ChangePassword

    ):

        user = self.get_profile(

            user_id

        )

        if not verify_password(

            data.old_password,

            user.password_hash

        ):

            raise InvalidCredentialsException()

        user.password_hash = hash_password(

            data.new_password

        )

        user = self.repository.update(

            user

        )

        info(

            f"Password changed: {user.email}"

        )

        return user

    # ------------------------------------------------------
    # UPDATE AVATAR
    # ------------------------------------------------------

    def update_avatar(

        self,

        user_id: int,

        avatar: str

    ):

        user = self.get_profile(

            user_id

        )

        user.profile_image = avatar

        user = self.repository.update(

            user

        )

        info(

            f"Avatar updated: {user.email}"

        )

        return user