# ==========================================================
# PDF MASTER AI
# Watermark PDF Service
# ==========================================================

# ----------------------------------------------------------
# IMPORT
# ----------------------------------------------------------

from pypdf import PdfReader
from pypdf import PdfWriter

from services.pdf.base_pdf_service import BasePdfService

# ----------------------------------------------------------
# WATERMARK SERVICE
# ----------------------------------------------------------

class WatermarkService(BasePdfService):

    """
    PDF Watermark Service.
    """

    def __init__(self, db):

        super().__init__(db)

    # ------------------------------------------------------
    # APPLY WATERMARK
    # ------------------------------------------------------

    def apply_watermark(

        self,

        input_path: str,

        watermark_path: str,

        output_path: str,

        first_page_only: bool = False

    ) -> str:

        reader = PdfReader(input_path)

        watermark_reader = PdfReader(watermark_path)

        watermark_page = watermark_reader.pages[0]

        writer = PdfWriter()

        for index, page in enumerate(reader.pages):

            if not first_page_only or index == 0:

                page.merge_page(watermark_page)

            writer.add_page(page)

        with open(output_path, "wb") as pdf:

            writer.write(pdf)

        writer.close()

        return output_path

    # ------------------------------------------------------
    # EXECUTE
    # ------------------------------------------------------

    def execute(

        self,

        file_id: int,

        watermark_path: str,

        output_path: str,

        first_page_only: bool = False

    ) -> str:

        file = self.get_file(file_id)

        self.validate_pdf(file)

        result = self.apply_watermark(

            file.file_path,

            watermark_path,

            output_path,

            first_page_only

        )

        self.save_history(

            file.user_id,

            file.id,

            "watermark_pdf"

        )

        self.log(

            f"Watermark added: {file.filename}"

        )

        return result