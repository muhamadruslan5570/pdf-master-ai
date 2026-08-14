import fitz
import os
import tempfile
import shutil

input_path = r".\storage\uploads\compressed\83f8f1ee105f41a9a55bde6852335df7_compressed_500kb_level_1.pdf"
output_path = r".\storage\uploads\compressed\test_font_optimized.pdf"

print()
print("==============================================")
print("PDF FONT OPTIMIZATION TEST")
print("==============================================")
print()

if not os.path.isfile(input_path):
    print("ERROR: Input PDF tidak ditemukan:")
    print(input_path)
    raise SystemExit(1)

before = os.path.getsize(input_path)

print("INPUT:")
print(input_path)
print()
print("BEFORE:", before, "bytes")
print("BEFORE:", round(before / 1024, 2), "KB")
print("BEFORE:", round(before / 1024 / 1024, 3), "MB")
print()

src = fitz.open(input_path)

print("PAGES :", src.page_count)
print("XREF  :", src.xref_length())
print()

# --------------------------------------------------
# ANALYZE FONT STREAMS
# --------------------------------------------------

font_streams = set()
font_descriptors = 0

for xref in range(1, src.xref_length()):

    typ = src.xref_get_key(
        xref,
        "Type"
    )

    if not isinstance(typ, tuple):
        continue

    if len(typ) < 2:
        continue

    if typ[1] != "/FontDescriptor":
        continue

    font_descriptors += 1

    for key in (
        "FontFile",
        "FontFile2",
        "FontFile3"
    ):

        value = src.xref_get_key(
            xref,
            key
        )

        if not isinstance(value, tuple):
            continue

        if len(value) < 2:
            continue

        if value[0] != "xref":
            continue

        try:
            stream_xref = int(
                value[1].split()[0]
            )
        except Exception:
            continue

        font_streams.add(
            stream_xref
        )

# --------------------------------------------------
# FONT SIZE
# --------------------------------------------------

font_bytes = 0

for xref in font_streams:

    raw = (
        src.xref_stream_raw(xref)
        or b""
    )

    font_bytes += len(raw)

print("FONT DESCRIPTORS :", font_descriptors)
print("UNIQUE FONT STREAMS :", len(font_streams))
print(
    "FONT STREAM SIZE :",
    font_bytes,
    "bytes"
)
print(
    "FONT STREAM SIZE :",
    round(font_bytes / 1024, 2),
    "KB"
)
print(
    "FONT STREAM SIZE :",
    round(font_bytes / 1024 / 1024, 3),
    "MB"
)

print()
print("----------------------------------------------")
print("TEST 1: MuPDF structural optimization")
print("----------------------------------------------")
print()

# --------------------------------------------------
# TEST SAFE STRUCTURAL SAVE
# --------------------------------------------------

src.save(
    output_path,
    garbage=4,
    clean=True,
    deflate=True,
    deflate_images=True,
    deflate_fonts=True
)

src.close()

after = os.path.getsize(output_path)

print("OUTPUT:")
print(output_path)
print()

print("BEFORE :", before, "bytes")
print("AFTER  :", after, "bytes")
print("SAVED  :", before - after, "bytes")

if before > 0:

    reduction = (
        (before - after)
        / before
        * 100
    )

    print(
        "REDUCTION:",
        round(reduction, 2),
        "%"
    )

print()

# --------------------------------------------------
# INTERPRETATION
# --------------------------------------------------

if after < before:

    print("RESULT: PDF BERHASIL DIPERKECIL.")
    print()
    print(
        "Structural optimization memberikan hasil."
    )

elif after == before:

    print(
        "RESULT: UKURAN TIDAK BERUBAH."
    )
    print()
    print(
        "MuPDF tidak menemukan optimasi struktural "
        "tambahan yang signifikan."
    )

else:

    print(
        "RESULT: HASIL MALAH LEBIH BESAR."
    )
    print()
    print(
        "Jangan gunakan hasil ini sebagai compressor."
    )

print()
print("==============================================")
print("TEST SELESAI")
print("==============================================")
