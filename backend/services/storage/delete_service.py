# ==========================================================
# PDF MASTER AI
# Delete Service
# ==========================================================

# ----------------------------------------------------------
# IMPORT
# ----------------------------------------------------------

from sqlalchemy.orm import Session

from repositories.file_repository import FileRepository

from services.storage.local_storage_service import (
    LocalStorageService
)

from exceptions.database import (
    RecordNotFoundException
)


# ----------------------------------------------------------
# DELETE SERVICE
# ----------------------------------------------------------

class DeleteService(LocalStorageService):

    """
    Delete Service.
    """

    def __init__(
        self,
        db: Session
    ):

        super().__init__(db)

        self.repository = FileRepository(
            db
        )

    # ------------------------------------------------------
    # GET FILE
    # ------------------------------------------------------

    def get(
        self,
        file_id: int
    ):

        file = self.repository.get_by_id(
            file_id
        )

        if file is None:

            raise RecordNotFoundException(
                "File"
            )

        return file

    # ------------------------------------------------------
    # SOFT DELETE
    # ------------------------------------------------------

    def soft_delete(
        self,
        file_id: int
    ):

        """
        Soft delete is not available because
        File model does not currently define
        an is_deleted field.
        """

        file = self.get(
            file_id
        )

        return file

    # ------------------------------------------------------
    # HARD DELETE
    # ------------------------------------------------------

    def hard_delete(
        self,
        file_id: int
    ) -> bool:

        file = self.get(
            file_id
        )

        if self.exists(
            file.storage_path
        ):

            self.remove(
                file.storage_path
            )

        self.save_history(
            file.user_id,
            file.id,
            "hard_delete"
        )

        self.repository.delete(
            file
        )

        self.log(
            f"Hard delete: {file.original_name}"
        )

        return True

    # ------------------------------------------------------
    # DELETE ALL USER FILES
    # ------------------------------------------------------

    def hard_delete_all(
        self,
        user_id: int
    ) -> int:

        """
        Delete all files belonging to one user.
        """

        files = self.repository.get_by_user(
            user_id
        )

        deleted = 0

        for file in files:

            self.hard_delete(
                file.id
            )

            deleted += 1

        return deleted
    # ------------------------------------------------------
    # DELETE FILE ONLY
    # ------------------------------------------------------

    def delete_storage(
        self,
        file_id: int
    ) -> bool:

        file = self.get(
            file_id
        )

        if not self.exists(
            file.storage_path
        ):

            return False

        self.remove(
            file.storage_path
        )

        self.save_history(
            file.user_id,
            file.id,
            "delete_storage"
        )

        self.log(
            f"Delete storage: {file.original_name}"
        )

        return True

    # ------------------------------------------------------
    # DELETE DATABASE ONLY
    # ------------------------------------------------------

    def delete_database(
        self,
        file_id: int
    ) -> bool:

        file = self.get(
            file_id
        )

        self.repository.delete(
            file
        )

        self.log(
            f"Delete database: {file.original_name}"
        )

        return True