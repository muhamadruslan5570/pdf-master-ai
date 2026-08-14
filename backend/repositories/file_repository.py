# ==========================================================
# PDF MASTER AI
# File Repository
# ==========================================================

# ----------------------------------------------------------
# IMPORT
# ----------------------------------------------------------

from sqlalchemy.orm import Session

from models.file import File

from repositories.base_repository import BaseRepository


# ----------------------------------------------------------
# FILE REPOSITORY
# ----------------------------------------------------------

class FileRepository(
    BaseRepository[File]
):

    """
    File Repository.
    """

    def __init__(
        self,
        db: Session
    ):

        super().__init__(
            db,
            File
        )

    # ------------------------------------------------------
    # GET USER FILES
    # ------------------------------------------------------

    def get_by_user(
        self,
        user_id: int
    ) -> list[File]:

        return (
            self.db.query(File)
            .filter(
                File.user_id == user_id
            )
            .order_by(
                File.created_at.desc()
            )
            .all()
        )

    # ------------------------------------------------------
    # GET FILE NAME
    # ------------------------------------------------------

    def get_by_filename(
        self,
        filename: str
    ) -> File | None:

        return (
            self.db.query(File)
            .filter(
                File.original_name == filename
            )
            .first()
        )

    # ------------------------------------------------------
    # GET FILE TYPE
    # ------------------------------------------------------

    def get_by_type(
        self,
        file_type: str
    ) -> list[File]:

        return (
            self.db.query(File)
            .filter(
                File.mime_type == file_type
            )
            .all()
        )

    # ------------------------------------------------------
    # GET STATUS
    # ------------------------------------------------------

    def get_by_status(
        self,
        status: str
    ) -> list[File]:

        return (
            self.db.query(File)
            .filter(
                File.status == status
            )
            .all()
        )

    # ------------------------------------------------------
    # FILE EXISTS
    # ------------------------------------------------------

    def filename_exists(
        self,
        filename: str
    ) -> bool:

        return (
            self.get_by_filename(
                filename
            )
            is not None
        )

    # ------------------------------------------------------
    # UPDATE STATUS
    # ------------------------------------------------------

    def update_status(
        self,
        file: File,
        status: str
    ) -> File:

        file.status = status

        self.db.commit()

        self.db.refresh(
            file
        )

        return file