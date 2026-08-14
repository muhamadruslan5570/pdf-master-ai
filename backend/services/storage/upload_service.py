# ==========================================================
# PDF MASTER AI
# Upload Service
# ==========================================================

# ----------------------------------------------------------
# IMPORT
# ----------------------------------------------------------

from pathlib import Path
from uuid import uuid4

from fastapi import UploadFile
from sqlalchemy.orm import Session

from models.file import File

from repositories.file_repository import FileRepository

from services.storage.local_storage_service import (
    LocalStorageService
)

from core.logger import info

# ----------------------------------------------------------
# UPLOAD SERVICE
# ----------------------------------------------------------

class UploadService(LocalStorageService):

    """
    Upload Service.
    """

    def __init__(

        self,

        db: Session

    ):

        super().__init__(db)

        self.repository = FileRepository(db)

    # ------------------------------------------------------
    # GENERATE NAME
    # ------------------------------------------------------

    def generate_filename(

        self,

        filename: str

    ) -> str:

        extension = Path(filename).suffix.lower()

        return f"{uuid4().hex}{extension}"

    # ------------------------------------------------------
    # UPLOAD
    # ------------------------------------------------------

    def upload(

        self,

        upload_file: UploadFile,

        upload_directory: str,

        user_id: int

    ) -> File:

        self.create_folder(

            upload_directory

        )

        filename = self.generate_filename(

            upload_file.filename

        )

        destination = (

            Path(upload_directory)

            / filename

        )

        self.save(

            upload_file,

            str(destination)

        )

        file = File(

    user_id=user_id,

    original_name=upload_file.filename,

    stored_name=filename,

    file_extension=destination.suffix.lower(),

    mime_type=upload_file.content_type,

    file_size=destination.stat().st_size,

    storage_path=str(destination),

    status="uploaded"

)

        file = self.repository.create(

            file

        )

        self.save_history(

            user_id,

            file.id,

            "upload"

        )

        self.log(

            f"Uploaded: {filename}"

        )

        return file

    # ------------------------------------------------------
    # MULTIPLE UPLOAD
    # ------------------------------------------------------

    def upload_multiple(

        self,

        files: list[UploadFile],

        upload_directory: str,

        user_id: int

    ) -> list[File]:

        uploaded = []

        for file in files:

            uploaded.append(

                self.upload(

                    file,

                    upload_directory,

                    user_id

                )

            )

        return uploaded