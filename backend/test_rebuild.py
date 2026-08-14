import fitz
import os
import io
from PIL import Image

input_path = r".\storage\uploads\compressed\83f8f1ee105f41a9a55bde6852335df7_compressed_500kb_level_1.pdf"

output_path = r".\storage\uploads\compressed\test_rebuild_72dpi_q50_pillow.pdf"

dpi = 72
quality = 50

src = fitz.open(input_path)
dst = fitz.open()

matrix = fitz.Matrix(
    dpi / 72,
    dpi / 72
)

for page_number, page in enumerate(src, start=1):

    pix = page.get_pixmap(
        matrix=matrix,
        alpha=False
    )

    image = Image.frombytes(
        "RGB",
        [pix.width, pix.height],
        pix.samples
    )

    buffer = io.BytesIO()

    image.save(
        buffer,
        format="JPEG",
        quality=quality,
        optimize=True
    )

    jpeg_bytes = buffer.getvalue()

    print(
        f"Page {page_number}: "
        f"{pix.width}x{pix.height} | "
        f"JPEG={len(jpeg_bytes):,} bytes"
    )

    rect = fitz.Rect(
        0,
        0,
        pix.width,
        pix.height
    )

    new_page = dst.new_page(
        width=rect.width,
        height=rect.height
    )

    new_page.insert_image(
        rect,
        stream=jpeg_bytes
    )

dst.save(
    output_path,
    garbage=4,
    deflate=True,
    clean=True
)

dst.close()
src.close()

before = os.path.getsize(input_path)
after = os.path.getsize(output_path)

print()
print("==============================")
print("REBUILD TEST RESULT")
print("==============================")
print("BEFORE :", before, "bytes")
print("AFTER  :", after, "bytes")
print("BEFORE :", round(before / 1024, 2), "KB")
print("AFTER  :", round(after / 1024, 2), "KB")
print("SAVED  :", before - after, "bytes")

if before:
    print(
        "REDUCTION:",
        round(
            ((before - after) / before) * 100,
            2
        ),
        "%"
    )

print()
print("OUTPUT:", output_path)
