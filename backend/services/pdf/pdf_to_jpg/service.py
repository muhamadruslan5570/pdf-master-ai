# ==========================================================
# PDF MASTER AI
# PDF TO JPG SERVICE
# ==========================================================

from pathlib import Path
from typing import Optional
import pymupdf


def parse_pages_string(pages_str: Optional[str], total_pages: int) -> list[int]:
    """
    Mengubah string pilihan halaman (1-based) dari user ('2', '1-3', '1,3,5')
    menjadi daftar indeks halaman 0-based yang valid untuk PyMuPDF.
    """
    if not pages_str or not str(pages_str).strip():
        return list(range(total_pages))  # Jika kosong, ambil semua halaman

    selected = set()
    parts = str(pages_str).split(",")

    for part in parts:
        part = part.strip()
        if "-" in part:
            try:
                start_str, end_str = part.split("-", 1)
                start = int(start_str.strip())
                end = int(end_str.strip())
                for p in range(start - 1, end):
                    if 0 <= p < total_pages:
                        selected.add(p)
            except ValueError:
                continue
        elif part.isdigit():
            p = int(part) - 1
            if 0 <= p < total_pages:
                selected.add(p)

    result = sorted(list(selected))
    return result if result else list(range(total_pages))


class PdfToJpgService:

    def __init__(self, db=None):
        self.db = db

    # ------------------------------------------------------
    # CONVERT PDF TO JPG
    # ------------------------------------------------------

    def convert(
        self,
        pdf_path: str,
        output_directory: str,
        dpi: int = 150,
        pages: Optional[str] = None
    ) -> list[str]:

        pdf_path = Path(pdf_path)
        output_directory = Path(output_directory)

        if not pdf_path.exists():
            raise FileNotFoundError(str(pdf_path))

        output_directory.mkdir(parents=True, exist_ok=True)

        document = pymupdf.open(str(pdf_path))
        output_files = []

        try:
            total_pages = len(document)
            target_indices = parse_pages_string(pages, total_pages)

            for page_index in target_indices:
                page = document.load_page(page_index)
                page_number = page_index + 1  # 1-based page number untuk nama file

                pixmap = page.get_pixmap(
                    dpi=dpi,
                    colorspace=pymupdf.csRGB,
                    alpha=False
                )

                output_path = (
                    output_directory /
                    f"{pdf_path.stem}_page_{page_number}.jpg"
                )

                pixmap.save(str(output_path))
                output_files.append(str(output_path))

        finally:
            document.close()

        if not output_files:
            raise ValueError("Tidak ada halaman yang berhasil dikonversi.")

        return output_files
