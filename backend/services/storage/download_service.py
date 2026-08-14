# ==========================================================
# PDF MASTER AI
# Download Service
# ==========================================================

# ----------------------------------------------------------
# IMPORT
# ----------------------------------------------------------

from pathlib import Path

from fastapi.responses import FileResponse

from sqlalchemy.orm import Session

from repositories.file_repository import FileRepository

from services.storage.local_storage_service import (
    LocalStorageService
)

from exceptions.database import (
    RecordNotFoundException
)

# ----------------------------------------------------------
# DOWNLOAD SERVICE
# ----------------------------------------------------------

class DownloadService(LocalStorageService):

    """
    Download Service.
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
    # DOWNLOAD
    # ------------------------------------------------------

    def download(
        self,
        file_id: int
    ) -> FileResponse:

        file = self.repository.get_by_id(
            file_id
        )

        if file is None:

            raise RecordNotFoundException(
                "File"
            )

        file_path = file.storage_path

        if not self.exists(
            file_path
        ):

            raise FileNotFoundError(
                file_path
            )

        self.save_history(
            file.user_id,
            file.id,
            "download"
        )

        self.log(
            f"Downloaded: {file.original_name}"
        )

        return FileResponse(
            path=file_path,
            filename=file.original_name,
            media_type=file.mime_type
        )

    # ------------------------------------------------------
    # DOWNLOAD PATH
    # ------------------------------------------------------

    def download_path(
        self,
        path: str
    ) -> FileResponse:

        file = Path(
            path
        )

        if not file.exists():

            raise FileNotFoundError(
                path
            )

        return FileResponse(
            path=str(file),
            filename=file.name
        )

    # ------------------------------------------------------
    # FILE INFO
    # ------------------------------------------------------

    def info(
        self,
        file_id: int
    ) -> dict:

        file = self.repository.get_by_id(
            file_id
        )

        if file is None:

            raise RecordNotFoundException(
                "File"
            )

        return {
            "id": file.id,
            "filename": file.original_name,
            "original_filename": file.original_name,
            "mime_type": file.mime_type,
            "size": file.file_size,
            "downloads": getattr(
                file,
                "download_count",
                0
            ),
            "status": file.status
        }