# ==========================================================
# PDF MASTER AI
# History Repository
# ==========================================================

# ----------------------------------------------------------
# IMPORT
# ----------------------------------------------------------

from sqlalchemy.orm import Session

from models.history import History

from repositories.base_repository import BaseRepository

# ----------------------------------------------------------
# HISTORY REPOSITORY
# ----------------------------------------------------------

class HistoryRepository(

    BaseRepository[History]

):

    """
    History Repository.
    """

    def __init__(

        self,

        db: Session

    ):

        super().__init__(

            db,

            History

        )

    # ------------------------------------------------------
    # GET USER HISTORY
    # ------------------------------------------------------

    def get_by_user(

        self,

        user_id: int

    ) -> list[History]:

        return (

            self.db.query(History)

            .filter(

                History.user_id == user_id

            )

            .order_by(

                History.created_at.desc()

            )

            .all()

        )

    # ------------------------------------------------------
    # GET ACTION
    # ------------------------------------------------------

    def get_by_action(

        self,

        action: str

    ) -> list[History]:

        return (

            self.db.query(History)

            .filter(

                History.action == action

            )

            .order_by(

                History.created_at.desc()

            )

            .all()

        )

    # ------------------------------------------------------
    # GET USER ACTION
    # ------------------------------------------------------

    def get_user_action(

        self,

        user_id: int,

        action: str

    ) -> list[History]:

        return (

            self.db.query(History)

            .filter(

                History.user_id == user_id,

                History.action == action

            )

            .order_by(

                History.created_at.desc()

            )

            .all()

        )

    # ------------------------------------------------------
    # GET FILE HISTORY
    # ------------------------------------------------------

    def get_by_file(

        self,

        file_id: int

    ) -> list[History]:

        return (

            self.db.query(History)

            .filter(

                History.file_id == file_id

            )

            .order_by(

                History.created_at.desc()

            )

            .all()

        )

    # ------------------------------------------------------
    # DELETE USER HISTORY
    # ------------------------------------------------------

    def delete_by_user(

        self,

        user_id: int

    ) -> int:

        deleted = (

            self.db.query(History)

            .filter(

                History.user_id == user_id

            )

            .delete()

        )

        self.db.commit()

        return deleted

    # ------------------------------------------------------
    # DELETE FILE HISTORY
    # ------------------------------------------------------

    def delete_by_file(

        self,

        file_id: int

    ) -> int:

        deleted = (

            self.db.query(History)

            .filter(

                History.file_id == file_id

            )

            .delete()

        )

        self.db.commit()

        return deleted

    # ------------------------------------------------------
    # COUNT USER HISTORY
    # ------------------------------------------------------

    def count_by_user(

        self,

        user_id: int

    ) -> int:

        return (

            self.db.query(History)

            .filter(

                History.user_id == user_id

            )

            .count()

        )

    # ------------------------------------------------------
    # COUNT ACTION
    # ------------------------------------------------------

    def count_by_action(

        self,

        action: str

    ) -> int:

        return (

            self.db.query(History)

            .filter(

                History.action == action

            )

            .count()

        )