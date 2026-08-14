# ==========================================================
# PDF MASTER AI
# Rotate PDF Service
# ==========================================================

# ----------------------------------------------------------
# IMPORT
# ----------------------------------------------------------

from pypdf import PdfReader
from pypdf import PdfWriter

from services.pdf.base_pdf_service import BasePdfService

# ----------------------------------------------------------
# ROTATE SERVICE
# ----------------------------------------------------------

class RotateService(

    BasePdfService

):

    """
    PDF Rotate Service.
    """

    def __init__(

        self,

        db

    ):

        super().__init__(db)

    # ------------------------------------------------------
    # ROTATE
    # ------------------------------------------------------

    def rotate(

        self,

        input_path: str,

        output_path: str,

        angle: int = 90

    ) -> str:

        reader = PdfReader(

            input_path

        )

        writer = PdfWriter()

        for page in reader.pages:

            page.rotate(

                angle

            )

            writer.add_page(

                page

            )

        with open(

            output_path,

            "wb"

        ) as pdf:

            writer.write(

                pdf

            )

        return output_path

    # ------------------------------------------------------
    # EXECUTE
    # ------------------------------------------------------

    def execute(

        self,

        file_id: int,

        output_path: str,

        angle: int = 90

    ) -> str:

        file = self.get_file(

            file_id

        )

        self.validate_pdf(

            file

        )

        result = self.rotate(

            file.file_path,

            output_path,

            angle

        )

        self.save_history(

            file.user_id,

            file.id,

            "rotate_pdf"

        )

        self.log(

            f"Rotate PDF: {file.filename}"

        )

        return result