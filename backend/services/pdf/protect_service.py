# ==========================================================
# PDF MASTER AI
# Protect PDF Service
# ==========================================================

from pypdf import PdfReader
from pypdf import PdfWriter

from services.pdf.base_pdf_service import BasePdfService


class ProtectService(BasePdfService):

    """
    PDF Protect Service.
    """

    def __init__(self, db):

        super().__init__(db)

    # ------------------------------------------------------

    def protect(

        self,

        input_path: str,

        output_path: str,

        password: str

    ) -> str:

        reader = PdfReader(input_path)

        writer = PdfWriter()

        for page in reader.pages:

            writer.add_page(page)

        writer.encrypt(password)

        with open(output_path, "wb") as pdf:

            writer.write(pdf)

        return output_path

    # ------------------------------------------------------

    def execute(

        self,

        file_id: int,

        output_path: str,

        password: str

    ) -> str:

        file = self.get_file(file_id)

        self.validate_pdf(file)

        result = self.protect(

            file.file_path,

            output_path,

            password

        )

        self.save_history(

            file.user_id,

            file.id,

            "protect_pdf"

        )

        self.log(

            f"Protect PDF: {file.filename}"

        )

        return result