# ==========================================================
# PDF MASTER AI
# Image Utilities
# ==========================================================

# ----------------------------------------------------------
# IMPORT
# ----------------------------------------------------------

from pathlib import Path

from PIL import Image

# ----------------------------------------------------------
# IMAGE EXISTS
# ----------------------------------------------------------

def is_image(

    file_path: str

) -> bool:
    """
    Check image extension.
    """

    return Path(

        file_path

    ).suffix.lower() in (

        ".jpg",

        ".jpeg",

        ".png",

        ".gif",

        ".bmp",

        ".tiff",

        ".webp"

    )

# ----------------------------------------------------------
# IMAGE SIZE
# ----------------------------------------------------------

def get_image_size(

    file_path: str

) -> tuple[int, int]:
    """
    Get image width and height.
    """

    with Image.open(file_path) as image:

        return image.size

# ----------------------------------------------------------
# IMAGE FORMAT
# ----------------------------------------------------------

def get_image_format(

    file_path: str

) -> str:
    """
    Get image format.
    """

    with Image.open(file_path) as image:

        return image.format

# ----------------------------------------------------------
# IMAGE MODE
# ----------------------------------------------------------

def get_image_mode(

    file_path: str

) -> str:
    """
    Get image mode.
    """

    with Image.open(file_path) as image:

        return image.mode

# ----------------------------------------------------------
# RESIZE IMAGE
# ----------------------------------------------------------

def resize_image(

    input_path: str,

    output_path: str,

    width: int,

    height: int

) -> None:
    """
    Resize image.
    """

    with Image.open(input_path) as image:

        resized = image.resize(

            (width, height)

        )

        resized.save(output_path)

# ----------------------------------------------------------
# CONVERT IMAGE
# ----------------------------------------------------------

def convert_image(

    input_path: str,

    output_path: str,

    format: str

) -> None:
    """
    Convert image format.
    """

    with Image.open(input_path) as image:

        image.save(

            output_path,

            format=format.upper()

        )

# ----------------------------------------------------------
# COMPRESS IMAGE
# ----------------------------------------------------------

def compress_image(

    input_path: str,

    output_path: str,

    quality: int = 80

) -> None:
    """
    Compress image.
    """

    with Image.open(input_path) as image:

        image.save(

            output_path,

            optimize=True,

            quality=quality

        )

# ----------------------------------------------------------
# THUMBNAIL
# ----------------------------------------------------------

def create_thumbnail(

    input_path: str,

    output_path: str,

    size: tuple[int, int] = (300, 300)

) -> None:
    """
    Create thumbnail.
    """

    with Image.open(input_path) as image:

        image.thumbnail(size)

        image.save(output_path)