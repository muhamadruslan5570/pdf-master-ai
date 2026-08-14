# ==========================================================
# PDF MASTER AI
# Metadata Service
# ==========================================================

# ----------------------------------------------------------
# IMPORT
# ----------------------------------------------------------

from pathlib import Path

from pypdf import PdfReader

from services.pdf.base_pdf_service import BasePdfService

# ----------------------------------------------------------
# METADATA SERVICE
# ----------------------------------------------------------

class MetadataService(BasePdfService):

    """
    PDF Metadata Service.
    """

    def __init__(self, db):

        super().__init__(db)

    # ------------------------------------------------------
    # DOCUMENT INFO
    # ------------------------------------------------------

    def get_document_info(

        self,

        reader: PdfReader

    ) -> dict:

        meta = reader.metadata or {}

        return {

            "title": meta.get("/Title"),

            "author": meta.get("/Author"),

            "subject": meta.get("/Subject"),

            "keywords": meta.get("/Keywords"),

            "creator": meta.get("/Creator"),

            "producer": meta.get("/Producer"),

            "creation_date": meta.get("/CreationDate"),

            "modification_date": meta.get("/ModDate")

        }

    # ------------------------------------------------------
    # FILE INFO
    # ------------------------------------------------------

    def get_file_info(

        self,

        input_path: str

    ) -> dict:

        path = Path(input_path)

        stat = path.stat()

        return {

            "filename": path.name,

            "extension": path.suffix,

            "directory": str(path.parent),

            "size_bytes": stat.st_size

        }

    # ------------------------------------------------------
    # PAGE INFO
    # ------------------------------------------------------

    def get_page_info(

        self,

        reader: PdfReader

    ) -> dict:

        pages = len(reader.pages)

        widths = []

        heights = []

        for page in reader.pages:

            box = page.mediabox

            widths.append(float(box.width))

            heights.append(float(box.height))

        return {

            "total_pages": pages,

            "page_width": widths,

            "page_height": heights

        }

    # ------------------------------------------------------
    # SECURITY
    # ------------------------------------------------------

    def get_security_info(

        self,

        reader: PdfReader

    ) -> dict:

        return {

            "encrypted": reader.is_encrypted

        }

    # ------------------------------------------------------
    # PERMISSIONS
    # ------------------------------------------------------

    def get_permissions(

        self,

        reader: PdfReader

    ) -> dict:

        permissions = {}

        if hasattr(reader, "decode_permissions"):

            try:

                permissions = reader.decode_permissions()

            except Exception:

                permissions = {}

        return permissions

    # ------------------------------------------------------
    # FONTS
    # ------------------------------------------------------

    def get_fonts(

        self,

        reader: PdfReader

    ) -> list:

        fonts = set()

        for page in reader.pages:

            resources = page.get("/Resources")

            if not resources:

                continue

            font_dict = resources.get("/Font")

            if not font_dict:

                continue

            for font in font_dict.keys():

                fonts.add(str(font))

        return sorted(list(fonts))

    # ------------------------------------------------------
    # IMAGES
    # ------------------------------------------------------

    def get_images(

        self,

        reader: PdfReader

    ) -> int:

        total = 0

        for page in reader.pages:

            resources = page.get("/Resources")

            if not resources:

                continue

            xobject = resources.get("/XObject")

            if not xobject:

                continue

            for obj in xobject.values():

                try:

                    if obj.get("/Subtype") == "/Image":

                        total += 1
                except Exception:

                    pass

        return total

    # ------------------------------------------------------
    # BOOKMARKS
    # ------------------------------------------------------

    def get_bookmarks(

        self,

        reader: PdfReader

    ):

        try:

            return reader.outline

        except Exception:

            return []

    # ------------------------------------------------------
    # XMP
    # ------------------------------------------------------

    def get_xmp_metadata(

        self,

        reader: PdfReader

    ):

        try:

            return reader.xmp_metadata

        except Exception:

            return None

    # ------------------------------------------------------
    # EXECUTE
    # ------------------------------------------------------

    def execute(

        self,

        file_id: int

    ) -> dict:

        file = self.get_file(file_id)

        self.validate_pdf(file)

        reader = PdfReader(file.file_path)

        self.save_history(

            file.user_id,

            file.id,

            "metadata_pdf"

        )

        self.log(

            f"Metadata PDF: {file.filename}"

        )

        return {

            "document": self.get_document_info(reader),

            "file": self.get_file_info(file.file_path),

            "pages": self.get_page_info(reader),

            "security": self.get_security_info(reader),

            "permissions": self.get_permissions(reader),

            "fonts": self.get_fonts(reader),

            "images": self.get_images(reader),

            "bookmarks": self.get_bookmarks(reader),

            "xmp": self.get_xmp_metadata(reader)

        }