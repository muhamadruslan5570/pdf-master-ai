# ==========================================================
# PDF MASTER AI
# Unlock PDF Service
# ==========================================================

# ----------------------------------------------------------
# IMPORT
# ----------------------------------------------------------

from pypdf import PdfReader
from pypdf import PdfWriter

from services.pdf.base_pdf_service import BasePdfService

# ----------------------------------------------------------
# UNLOCK SERVICE
# ----------------------------------------------------------

class UnlockService(BasePdfService):

    """
    PDF Unlock Service.
    """

    def __init__(self, db):

        super().__init__(db)

    # ------------------------------------------------------
    # UNLOCK PDF
    # ------------------------------------------------------

    def unlock(

        self,

        input_path: str,

        output_path: str,

        password: str

    ) -> str:

        reader = PdfReader(input_path)

        if reader.is_encrypted:

            result = reader.decrypt(password)

            if result == 0:

                raise ValueError("Invalid PDF password.")

        writer = PdfWriter()

        for page in reader.pages:

            writer.add_page(page)

        with open(output_path, "wb") as pdf:

            writer.write(pdf)

        writer.close()

        return output_path

    # ------------------------------------------------------
    # CHECK ENCRYPTED
    # ------------------------------------------------------

    def is_encrypted(

        self,

        input_path: str

    ) -> bool:

        reader = PdfReader(input_path)

        return reader.is_encrypted

    # ------------------------------------------------------
    # EXECUTE
    # ------------------------------------------------------

    def execute(

        self,

        file_id: int,

        output_path: str,

        password: str

    ) -> str:

        file = self.get_file(file_id)

        self.validate_pdf(file)

        result = self.unlock(

            file.file_path,

            output_path,

            password

        )

        self.save_history(

            file.user_id,

            file.id,

            "unlock_pdf"

        )

        self.log(

            f"Unlocked PDF: {file.filename}"

        )

        return result