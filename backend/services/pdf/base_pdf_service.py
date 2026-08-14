# ==========================================================
# PDF MASTER AI
# Base PDF Service
# ==========================================================

# ----------------------------------------------------------
# IMPORT
# ----------------------------------------------------------

from sqlalchemy.orm import Session

from repositories.file_repository import FileRepository
from repositories.history_repository import HistoryRepository

from models.file import File
from models.history import History

from utils.file import (
    file_exists
)

from utils.pdf import (
    is_pdf
)

from core.logger import info

from exceptions.database import (
    RecordNotFoundException
)


# ----------------------------------------------------------
# BASE PDF SERVICE
# ----------------------------------------------------------

class BasePdfService:

    """
    Base PDF Service.
    """

    def __init__(
        self,
        db: Session
    ):

        self.db = db

        self.file_repository = FileRepository(
            db
        )

        self.history_repository = HistoryRepository(
            db
        )

    # ------------------------------------------------------
    # GET FILE
    # ------------------------------------------------------

    def get_file(
        self,
        file_id: int
    ) -> File:

        file = self.file_repository.get_by_id(
            file_id
        )

        if file is None:

            raise RecordNotFoundException(
                "File"
            )

        return file

    # ------------------------------------------------------
    # GET FILE PATH
    # ------------------------------------------------------

    def get_file_path(
        self,
        file: File
    ) -> str:

        """
        Get the physical storage path
        of the uploaded file.
        """

        return file.storage_path

    # ------------------------------------------------------
    # VALIDATE PDF
    # ------------------------------------------------------

    def validate_pdf(
        self,
        file: File
    ) -> None:

        file_path = self.get_file_path(
            file
        )

        if not file_exists(
            file_path
        ):

            raise FileNotFoundError(
                file_path
            )

        if not is_pdf(
            file_path
        ):

            raise ValueError(
                "Invalid PDF file."
            )

    # ------------------------------------------------------
    # SAVE HISTORY
    # ------------------------------------------------------

    def save_history(
        self,
        user_id: int,
        file_id: int,
        action: str
    ) -> None:

        history = History(
            user_id=user_id,
            file_id=file_id,
            action=action,
            category="pdf"
        )

        self.history_repository.create(
            history
        )

    # ------------------------------------------------------
    # LOG
    # ------------------------------------------------------

    def log(
        self,
        message: str
    ) -> None:

        info(
            message
        )