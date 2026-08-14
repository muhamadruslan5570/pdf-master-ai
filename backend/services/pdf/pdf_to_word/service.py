from pathlib import Path

import pymupdf
from docx import Document


class PdfToWordService:

    def __init__(self, db=None):
        self.db = db

    # ------------------------------------------------------
    # CONVERT PDF TO WORD
    # ------------------------------------------------------

    def convert(
        self,
        pdf_path: str,
        output_path: str
    ) -> str:

        pdf_path = Path(pdf_path)
        output_path = Path(output_path)

        if not pdf_path.exists():
            raise FileNotFoundError(
                str(pdf_path)
            )

        output_path.parent.mkdir(
            parents=True,
            exist_ok=True
        )

        document_pdf = pymupdf.open(
            str(pdf_path)
        )

        document_word = Document()

        try:

            for page_number, page in enumerate(
                document_pdf,
                start=1
            ):

                text = page.get_text("text")

                if text.strip():

                    document_word.add_paragraph(
                        text
                    )

                if page_number < len(document_pdf):

                    document_word.add_page_break()

        finally:

            document_pdf.close()

        document_word.save(
            str(output_path)
        )

        if not output_path.exists():

            raise ValueError(
                "File Word gagal dibuat."
            )

        return str(output_path)
