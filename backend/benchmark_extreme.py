import fitz
import os
import io
import time
from PIL import Image

# ============================================================
# INPUT
# ============================================================

input_path = r".\storage\uploads\compressed\83f8f1ee105f41a9a55bde6852335df7_compressed_500kb_level_1.pdf"

output_dir = r".\storage\uploads\compressed\test\benchmark"

os.makedirs(
    output_dir,
    exist_ok=True
)

# ============================================================
# 8 COMPRESSION COMBINATIONS
# ============================================================

tests = [
    {"dpi": 72, "quality": 50},
    {"dpi": 72, "quality": 35},
    {"dpi": 60, "quality": 50},
    {"dpi": 60, "quality": 35},
    {"dpi": 50, "quality": 40},
    {"dpi": 50, "quality": 30},
    {"dpi": 40, "quality": 35},
    {"dpi": 40, "quality": 25},
]

# ============================================================
# VALIDATE INPUT
# ============================================================

if not os.path.isfile(input_path):

    print()
    print("ERROR: Input PDF tidak ditemukan.")
    print(input_path)
    raise SystemExit(1)

before = os.path.getsize(
    input_path
)

print()
print("============================================================")
print("PDF EXTREME COMPRESSION BENCHMARK")
print("============================================================")
print()

print("INPUT:")
print(input_path)
print()

print(
    "ORIGINAL:",
    before,
    "bytes |",
    round(before / 1024, 2),
    "KB |",
    round(before / 1024 / 1024, 3),
    "MB"
)

print()
print("TOTAL TEST:", len(tests))
print()

# ============================================================
# RESULTS
# ============================================================

results = []

# ============================================================
# RUN TESTS
# ============================================================

for index, settings in enumerate(
    tests,
    start=1
):

    dpi = settings["dpi"]
    quality = settings["quality"]

    output_path = os.path.join(
        output_dir,
        f"benchmark_{dpi}dpi_q{quality}.pdf"
    )

    print()
    print("------------------------------------------------------------")
    print(
        f"TEST {index}/{len(tests)}"
    )
    print(
        f"DPI={dpi} | QUALITY={quality}"
    )
    print("------------------------------------------------------------")

    start_time = time.time()

    try:

        src = fitz.open(
            input_path
        )

        dst = fitz.open()

        matrix = fitz.Matrix(
            dpi / 72,
            dpi / 72
        )

        total_jpeg_bytes = 0

        for page_number, page in enumerate(
            src,
            start=1
        ):

            pix = page.get_pixmap(
                matrix=matrix,
                alpha=False
            )

            # ------------------------------------------------
            # Convert pixmap -> Pillow
            # ------------------------------------------------

            image = Image.frombytes(
                "RGB",
                [
                    pix.width,
                    pix.height
                ],
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

            total_jpeg_bytes += len(
                jpeg_bytes
            )

            # ------------------------------------------------
            # IMPORTANT:
            # Verify JPEG header before inserting
            # ------------------------------------------------

            if not (
                jpeg_bytes.startswith(b"\xff\xd8")
                and jpeg_bytes.endswith(b"\xff\xd9")
            ):

                raise RuntimeError(
                    f"Invalid JPEG generated "
                    f"on page {page_number}"
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

        # ----------------------------------------------------
        # SAVE
        # ----------------------------------------------------

        dst.save(
            output_path,
            garbage=4,
            deflate=True,
            clean=True
        )

        dst.close()
        src.close()

        # ----------------------------------------------------
        # SIZE
        # ----------------------------------------------------

        after = os.path.getsize(
            output_path
        )

        saved = (
            before - after
        )

        reduction = (
            saved / before * 100
            if before
            else 0
        )

        elapsed = (
            time.time()
            - start_time
        )

        result = {
            "test": index,
            "dpi": dpi,
            "quality": quality,
            "size": after,
            "saved": saved,
            "reduction": reduction,
            "jpeg_bytes": total_jpeg_bytes,
            "time": elapsed,
            "output": output_path
        }

        results.append(
            result
        )

        print()
        print(
            "BEFORE :",
            before,
            "bytes"
        )

        print(
            "AFTER  :",
            after,
            "bytes"
        )

        print(
            "AFTER  :",
            round(after / 1024, 2),
            "KB"
        )

        print(
            "SAVED  :",
            saved,
            "bytes"
        )

        print(
            "REDUCTION:",
            round(
                reduction,
                2
            ),
            "%"
        )

        print(
            "TIME:",
            round(
                elapsed,
                2
            ),
            "seconds"
        )

        print(
            "OUTPUT:",
            output_path
        )

    except Exception as exc:

        print()
        print(
            "ERROR:",
            exc
        )

        results.append(
            {
                "test": index,
                "dpi": dpi,
                "quality": quality,
                "size": None,
                "saved": None,
                "reduction": None,
                "jpeg_bytes": None,
                "time": None,
                "output": None,
                "error": str(exc)
            }
        )

        try:
            if "dst" in locals():
                dst.close()
        except Exception:
            pass

        try:
            if "src" in locals():
                src.close()
        except Exception:
            pass

# ============================================================
# SORT SUCCESSFUL RESULTS
# ============================================================

successful = [
    r
    for r in results
    if r.get("size") is not None
]

successful.sort(
    key=lambda r: r["size"]
)

# ============================================================
# FINAL REPORT
# ============================================================

print()
print()
print("============================================================")
print("BENCHMARK RESULT")
print("============================================================")
print()

print(
    f"{'RANK':<6}"
    f"{'DPI':<6}"
    f"{'QUALITY':<10}"
    f"{'SIZE KB':<14}"
    f"{'SAVED KB':<14}"
    f"{'REDUCTION':<12}"
)

print("-" * 70)

for rank, result in enumerate(
    successful,
    start=1
):

    size_kb = (
        result["size"]
        / 1024
    )

    saved_kb = (
        result["saved"]
        / 1024
    )

    print(
        f"{rank:<6}"
        f"{result['dpi']:<6}"
        f"{result['quality']:<10}"
        f"{size_kb:<14.2f}"
        f"{saved_kb:<14.2f}"
        f"{result['reduction']:<12.2f}%"
    )

print()

# ============================================================
# TARGET 500 KB
# ============================================================

target_bytes = 500 * 1024

under_target = [
    r
    for r in successful
    if r["size"] <= target_bytes
]

print("============================================================")
print("TARGET TEST")
print("============================================================")
print()

print(
    "TARGET:",
    target_bytes,
    "bytes"
)

print(
    "TARGET:",
    500,
    "KB"
)

print()

if under_target:

    # Pilih file terbesar yang masih <= target.
    # Tujuannya menjaga kualitas semaksimal mungkin.

    best_target = max(
        under_target,
        key=lambda r: r["size"]
    )

    print(
        "TARGET 500 KB BERHASIL DICAPAI."
    )

    print()

    print(
        "BEST PROFILE:"
    )

    print(
        f"DPI={best_target['dpi']} | "
        f"QUALITY={best_target['quality']}"
    )

    print(
        "SIZE:",
        round(
            best_target["size"] / 1024,
            2
        ),
        "KB"
    )

    print(
        "REDUCTION:",
        round(
            best_target["reduction"],
            2
        ),
        "%"
    )

    print(
        "OUTPUT:",
        best_target["output"]
    )

else:

    print(
        "TARGET 500 KB BELUM TERCAPAI."
    )

    print()

    if successful:

        smallest = successful[0]

        print(
            "HASIL TERKECIL:"
        )

        print(
            f"DPI={smallest['dpi']} | "
            f"QUALITY={smallest['quality']}"
        )

        print(
            "SIZE:",
            round(
                smallest["size"] / 1024,
                2
            ),
            "KB"
        )

        print(
            "REDUCTION:",
            round(
                smallest["reduction"],
                2
            ),
            "%"
        )

        print(
            "OUTPUT:",
            smallest["output"]
        )

print()
print("============================================================")
print("BENCHMARK SELESAI")
print("============================================================")
