# ==========================================================
# PDF MASTER AI
# Split PDF Service
# ==========================================================

# ----------------------------------------------------------
# IMPORT
# ----------------------------------------------------------

from pathlib import Path

from sqlalchemy.orm import Session

from pypdf import (

    PdfReader,

    PdfWriter

)

from repositories.file_repository import FileRepository

from repositories.history_repository import HistoryRepository

from models.file import File

from models.history import History

from utils.file import (

    create_directory,

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
# SPLIT SERVICE
# ----------------------------------------------------------

class SplitService:

    """
    PDF Split Service.
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

        file: File

    ) -> None:

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

                "Invalid PDF file."

            )

    # ------------------------------------------------------
    # SPLIT
    # ------------------------------------------------------

    def split(

        self,

        input_path: str,

        output_directory: str

    ) -> list[str]:

        create_directory(

            output_directory

        )

        reader = PdfReader(

            input_path

        )

        outputs = []

        stem = Path(

            input_path

        ).stem

        for index, page in enumerate(

            reader.pages,

            start=1

        ):

            writer = PdfWriter()

            writer.add_page(page)

            output_file = (

                Path(output_directory)

                / f"{stem}_page_{index}.pdf"

            )

            with open(

                output_file,

                "wb"

            ) as pdf:

                writer.write(

                    pdf

                )

            outputs.append(

                str(output_file)

            )

        return outputs

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

            action="split_pdf",

            category="pdf",

            status="completed"

        )

        self.history_repository.create(

            history

        )

    # ------------------------------------------------------
    # EXECUTE
    # ------------------------------------------------------

    def execute(

        self,

        file_id: int,

        output_directory: str

    ) -> list[str]:

        file = self.get_file(

            file_id

        )

        self.validate(

            file

        )

        result = self.split(

            file.storage_path,

            output_directory

        )

        self.save_history(

            file.user_id,

            file.id

        )

        info(

            f"Split PDF: {file.original_name}"

        )

        return result



