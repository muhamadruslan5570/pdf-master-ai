# ==========================================================
# PDF MASTER AI
# Base Storage Service
# ==========================================================

# ----------------------------------------------------------
# IMPORT
# ----------------------------------------------------------

from pathlib import Path

from sqlalchemy.orm import Session

from repositories.file_repository import FileRepository

from repositories.history_repository import HistoryRepository

from models.file import File

from models.history import History

from core.logger import info

from exceptions.database import (

    RecordNotFoundException

)

# ----------------------------------------------------------
# BASE STORAGE SERVICE
# ----------------------------------------------------------

class BaseStorageService:

    """
    Base Storage Service.
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
    # FILE EXISTS
    # ------------------------------------------------------

    def exists(

        self,

        path: str

    ) -> bool:

        return Path(path).exists()

    # ------------------------------------------------------
    # CREATE DIRECTORY
    # ------------------------------------------------------

    def create_directory(

        self,

        directory: str

    ) -> Path:

        path = Path(directory)

        path.mkdir(

            parents=True,

            exist_ok=True

        )

        return path

    # ------------------------------------------------------
    # DELETE FILE
    # ------------------------------------------------------

    def delete_file(

        self,

        path: str

    ) -> bool:

        file = Path(path)

        if file.exists():

            file.unlink()

            return True

        return False

    # ------------------------------------------------------
    # FILE SIZE
    # ------------------------------------------------------

    def file_size(

        self,

        path: str

    ) -> int:

        return Path(path).stat().st_size

    # ------------------------------------------------------
    # FILE NAME
    # ------------------------------------------------------

    def filename(

        self,

        path: str

    ) -> str:

        return Path(path).name

    # ------------------------------------------------------
    # EXTENSION
    # ------------------------------------------------------

    def extension(

        self,

        path: str

    ) -> str:

        return Path(path).suffix.lower()

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
	    category="storage"

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