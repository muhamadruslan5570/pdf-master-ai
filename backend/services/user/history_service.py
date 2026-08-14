# ==========================================================
# PDF MASTER AI
# History Service
# ==========================================================

# ----------------------------------------------------------
# IMPORT
# ----------------------------------------------------------

from sqlalchemy.orm import Session

from repositories.history_repository import HistoryRepository

from repositories.user_repository import UserRepository

from exceptions.database import (

    RecordNotFoundException

)

# ----------------------------------------------------------
# HISTORY SERVICE
# ----------------------------------------------------------

class HistoryService:

    """
    User History Service.
    """

    def __init__(

        self,

        db: Session

    ):

        self.history_repository = HistoryRepository(

            db

        )

        self.user_repository = UserRepository(

            db

        )

    # ------------------------------------------------------
    # GET USER
    # ------------------------------------------------------

    def get_user(

        self,

        user_id: int

    ):

        user = self.user_repository.get_by_id(

            user_id

        )

        if user is None:

            raise RecordNotFoundException(

                "User"

            )

        return user

    # ------------------------------------------------------
    # GET HISTORY
    # ------------------------------------------------------

    def get_history(

        self,

        user_id: int

    ):

        self.get_user(

            user_id

        )

        return self.history_repository.get_by_user(

            user_id

        )

    # ------------------------------------------------------
    # GET ACTION
    # ------------------------------------------------------

    def get_action(

        self,

        user_id: int,

        action: str

    ):

        self.get_user(

            user_id

        )

        return self.history_repository.get_user_action(

            user_id,

            action

        )

    # ------------------------------------------------------
    # GET FILE HISTORY
    # ------------------------------------------------------

    def get_file_history(

        self,

        file_id: int

    ):

        return self.history_repository.get_by_file(

            file_id

        )

    # ------------------------------------------------------
    # DELETE HISTORY
    # ------------------------------------------------------

    def delete_history(

        self,

        user_id: int

    ) -> int:

        self.get_user(

            user_id

        )

        return self.history_repository.delete_by_user(

            user_id

        )

    # ------------------------------------------------------
    # TOTAL HISTORY
    # ------------------------------------------------------

    def total_history(

        self,

        user_id: int

    ) -> int:

        self.get_user(

            user_id

        )

        return self.history_repository.count_by_user(

            user_id

        )

    # ------------------------------------------------------
    # TOTAL ACTION
    # ------------------------------------------------------

    def total_action(

        self,

        action: str

    ) -> int:

        return self.history_repository.count_by_action(

            action

        )