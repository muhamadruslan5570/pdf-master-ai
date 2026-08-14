# ==========================================================
# PDF MASTER AI
# Thumbnail PDF Service
# ==========================================================

# ----------------------------------------------------------
# IMPORT
# ----------------------------------------------------------

from pathlib import Path

import fitz

from services.pdf.base_pdf_service import BasePdfService

# ----------------------------------------------------------
# THUMBNAIL SERVICE
# ----------------------------------------------------------

class ThumbnailService(BasePdfService):

    """
    PDF Thumbnail Service.
    """

    def __init__(

        self,

        db

    ):

        super().__init__(db)

    # ------------------------------------------------------
    # GENERATE PAGE THUMBNAIL
    # ------------------------------------------------------

    def generate_thumbnail(

        self,

        input_path: str,

        output_image: str,

        page_number: int = 0,

        zoom: float = 2.0

    ) -> str:

        document = fitz.open(input_path)

        page = document.load_page(page_number)

        matrix = fitz.Matrix(

            zoom,

            zoom

        )

        pixmap = page.get_pixmap(

            matrix=matrix,

            alpha=False

        )

        Path(output_image).parent.mkdir(

            parents=True,

            exist_ok=True

        )

        pixmap.save(

            output_image

        )

        document.close()

        return output_image

    # ------------------------------------------------------
    # GENERATE ALL THUMBNAILS
    # ------------------------------------------------------

    def generate_all(

        self,

        input_path: str,

        output_directory: str,

        zoom: float = 2.0

    ) -> list[str]:

        document = fitz.open(input_path)

        Path(output_directory).mkdir(

            parents=True,

            exist_ok=True

        )

        outputs = []

        matrix = fitz.Matrix(

            zoom,

            zoom

        )

        for page_number in range(

            len(document)

        ):

            page = document.load_page(

                page_number

            )

            pixmap = page.get_pixmap(

                matrix=matrix,

                alpha=False

            )

            output = (

                Path(output_directory)

                / f"page_{page_number + 1}.png"

            )

            pixmap.save(

                output

            )

            outputs.append(

                str(output)

            )

        document.close()

        return outputs

    # ------------------------------------------------------
    # EXECUTE
    # ------------------------------------------------------

    def execute(

        self,

        file_id: int,

        output_directory: str,

        page_number: int = 0,

        all_pages: bool = False

    ):

        file = self.get_file(

            file_id

        )

        self.validate_pdf(

            file

        )

        if all_pages:

            result = self.generate_all(

                file.file_path,

                output_directory

            )

        else:

            output = (

                Path(output_directory)

                / "thumbnail.png"

            )

            result = self.generate_thumbnail(

                file.file_path,

                str(output),

                page_number

            )

        self.save_history(

            file.user_id,

            file.id,

            "thumbnail_pdf"

        )

        self.log(

            f"Thumbnail created: {file.filename}"

        )

        return result