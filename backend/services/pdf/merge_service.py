# ==========================================================
# PDF MASTER AI
# Merge PDF Service
# ==========================================================

# ----------------------------------------------------------
# IMPORT
# ----------------------------------------------------------

from sqlalchemy.orm import Session

from pypdf import PdfWriter

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
# MERGE SERVICE
# ----------------------------------------------------------

class MergeService:

    """
    PDF Merge Service.
    """

    def __init__(

        self,

        db: Session

    ):

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
    # VALIDATE
    # ------------------------------------------------------

    def validate(

        self,

        files: list[File]

    ) -> None:

        for file in files:

            if not file_exists(

                file.storage_path

            ):

                raise FileNotFoundError(

                    file.storage_path

                )

            if not is_pdf(

                file.storage_path

            ):

                raise ValueError(

                    "Invalid PDF."

                )

    # ------------------------------------------------------
    # MERGE PDF
    # ------------------------------------------------------

    def merge(

        self,

        files: list[File],

        output_path: str

    ) -> str:

        writer = PdfWriter()

        for file in files:

            writer.append(

                file.storage_path

            )

        with open(

            output_path,

            "wb"

        ) as pdf:

            writer.write(

                pdf

            )

        writer.close()

        return output_path

    # ------------------------------------------------------
    # SAVE HISTORY
    # ------------------------------------------------------

    def save_history(

        self,

        user_id: int,

        file_id: int

    ):

        history = History(

            user_id=user_id,

            file_id=file_id,

            action="merge_pdf",
        category="pdf"

        )

        self.history_repository.create(

            history

        )

    # ------------------------------------------------------
    # EXECUTE
    # ------------------------------------------------------

    def execute(

        self,

        file_ids: list[int],

        output_path: str

    ) -> str:

        files = [

            self.get_file(

                file_id

            )

            for file_id in file_ids

        ]

        self.validate(

            files

        )

        result = self.merge(

            files,

            output_path

        )

        self.save_history(

            files[0].user_id,

            files[0].id

        )

        info(

            f"Merged {len(files)} PDF files."

        )

        return result