# ==========================================================
# PDF MASTER AI
# Extract Service
# ==========================================================

# ----------------------------------------------------------
# IMPORT
# ----------------------------------------------------------

from pathlib import Path

import fitz

from pypdf import PdfReader
from pypdf import PdfWriter

from services.pdf.base_pdf_service import BasePdfService

# ----------------------------------------------------------
# EXTRACT SERVICE
# ----------------------------------------------------------

class ExtractService(BasePdfService):

    """
    PDF Extract Service.
    """

    def __init__(self, db):

        super().__init__(db)

    # ------------------------------------------------------
    # TEXT
    # ------------------------------------------------------

    def extract_text(

        self,

        input_path: str

    ) -> str:

        document = fitz.open(input_path)

        text = ""

        for page in document:

            text += page.get_text()

        document.close()

        return text

    # ------------------------------------------------------
    # IMAGES
    # ------------------------------------------------------

    def extract_images(

        self,

        input_path: str,

        output_directory: str

    ) -> list[str]:

        Path(output_directory).mkdir(

            parents=True,

            exist_ok=True

        )

        document = fitz.open(input_path)

        images = []

        for page_index in range(len(document)):

            page = document.load_page(page_index)

            image_list = page.get_images(full=True)

            for image_number, image in enumerate(image_list):

                xref = image[0]

                pix = fitz.Pixmap(

                    document,

                    xref

                )

                output = (

                    Path(output_directory)

                    / f"page_{page_index+1}_{image_number+1}.png"

                )

                if pix.n < 5:

                    pix.save(output)

                else:

                    rgb = fitz.Pixmap(

                        fitz.csRGB,

                        pix

                    )

                    rgb.save(output)

                    rgb = None

                pix = None

                images.append(

                    str(output)

                )

        document.close()

        return images

    # ------------------------------------------------------
    # LINKS
    # ------------------------------------------------------

    def extract_links(

        self,

        input_path: str

    ) -> list:

        document = fitz.open(input_path)

        links = []

        for page in document:

            links.extend(

                page.get_links()

            )

        document.close()

        return links

    # ------------------------------------------------------
    # FONTS
    # ------------------------------------------------------

    def extract_fonts(

        self,

        input_path: str

    ) -> list:

        document = fitz.open(input_path)

        fonts = []

        for page in document:

            fonts.extend(

                page.get_fonts()

            )

        document.close()

        return fonts

    # ------------------------------------------------------
    # ATTACHMENTS
    # ------------------------------------------------------

    def extract_attachments(

        self,

        input_path: str

    ) -> list:

        reader = PdfReader(input_path)

        attachments = []

        try:

            for name in reader.attachments:

                attachments.append(name)

        except Exception:

            pass

        return attachments

    # ------------------------------------------------------
    # PAGES
    # ------------------------------------------------------

    def extract_pages(

        self,

        input_path: str,

        output_directory: str

    ) -> list[str]:

        Path(output_directory).mkdir(

            parents=True,

            exist_ok=True

        )

        reader = PdfReader(input_path)

        outputs = []

        for index, page in enumerate(reader.pages):

            writer = PdfWriter()

            writer.add_page(page)

            output = (

                Path(output_directory)

                / f"page_{index+1}.pdf"

            )

            with open(output, "wb") as pdf:

                writer.write(pdf)

            outputs.append(

                str(output)

            )

        return outputs

    # ------------------------------------------------------
    # ANNOTATIONS
    # ------------------------------------------------------

    def extract_annotations(

        self,

        input_path: str

    ) -> list:

        document = fitz.open(input_path)

        annotations = []

        for page in document:

            annotation = page.first_annot

            while annotation:

                annotations.append(

                    annotation.info

                )

                annotation = annotation.next

        document.close()

        return annotations

    # ------------------------------------------------------
    # EXECUTE
    # ------------------------------------------------------

    def execute(

        self,

        file_id: int,

        output_directory: str

    ) -> dict:

        file = self.get_file(file_id)

        self.validate_pdf(file)

        self.save_history(

            file.user_id,

            file.id,

            "extract_pdf"

        )

        self.log(

            f"Extract PDF: {file.filename}"

        )

        return {

            "text": self.extract_text(

                file.file_path

            ),

            "images": self.extract_images(

                file.file_path,

                output_directory

            ),

            "links": self.extract_links(

                file.file_path

            ),

            "fonts": self.extract_fonts(

                file.file_path

            ),

            "attachments": self.extract_attachments(

                file.file_path

            ),

            "pages": self.extract_pages(

                file.file_path,

                output_directory

            ),

            "annotations": self.extract_annotations(

                file.file_path

            )

        }