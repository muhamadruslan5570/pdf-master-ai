# ==========================================================
# PDF MASTER AI
# User Repository
# ==========================================================

# ----------------------------------------------------------
# IMPORT
# ----------------------------------------------------------

from sqlalchemy.orm import Session

from models.user import User

from repositories.base_repository import BaseRepository


# ----------------------------------------------------------
# USER REPOSITORY
# ----------------------------------------------------------

class UserRepository(
    BaseRepository[User]
):

    """
    User Repository.
    """

    def __init__(
        self,
        db: Session
    ):

        super().__init__(
            db,
            User
        )

    # ------------------------------------------------------
    # GET BY EMAIL
    # ------------------------------------------------------

    def get_by_email(
        self,
        email: str
    ) -> User | None:

        return (
            self.db.query(User)
            .filter(
                User.email == email
            )
            .first()
        )

    # ------------------------------------------------------
    # GET BY USERNAME
    # ------------------------------------------------------

    def get_by_username(
        self,
        username: str
    ) -> User | None:

        return (
            self.db.query(User)
            .filter(
                User.username == username
            )
            .first()
        )

    # ------------------------------------------------------
    # EMAIL EXISTS
    # ------------------------------------------------------

    def email_exists(
        self,
        email: str
    ) -> bool:

        return (
            self.get_by_email(
                email
            )
            is not None
        )

    # ------------------------------------------------------
    # USERNAME EXISTS
    # ------------------------------------------------------

    def username_exists(
        self,
        username: str
    ) -> bool:

        return (
            self.get_by_username(
                username
            )
            is not None
        )

    # ------------------------------------------------------
    # GET ACTIVE USER
    # ------------------------------------------------------

    def get_active_user(
        self,
        user_id: int
    ) -> User | None:

        return (
            self.db.query(User)
            .filter(
                User.id == user_id,
                User.is_active.is_(True)
            )
            .first()
        )

    # ------------------------------------------------------
    # GET VERIFIED USER
    # ------------------------------------------------------

    def get_verified_user(
        self,
        user_id: int
    ) -> User | None:

        return (
            self.db.query(User)
            .filter(
                User.id == user_id,
                User.is_verified.is_(True)
            )
            .first()
        )

    # ------------------------------------------------------
    # GET ADMIN
    # ------------------------------------------------------

    def get_admins(
        self
    ) -> list[User]:

        return (
            self.db.query(User)
            .filter(
                User.is_admin.is_(True)
            )
            .all()
        )

    # ------------------------------------------------------
    # ACTIVATE USER
    # ------------------------------------------------------

    def activate(
        self,
        user: User
    ) -> User:

        user.is_active = True

        self.db.commit()

        self.db.refresh(
            user
        )

        return user

    # ------------------------------------------------------
    # VERIFY USER
    # ------------------------------------------------------

    def verify(
        self,
        user: User
    ) -> User:

        user.is_verified = True

        self.db.commit()

        self.db.refresh(
            user
        )

        return user

    # ------------------------------------------------------
    # DEACTIVATE USER
    # ------------------------------------------------------

    def deactivate(
        self,
        user: User
    ) -> User:

        user.is_active = False

        self.db.commit()

        self.db.refresh(
            user
        )

        return user
