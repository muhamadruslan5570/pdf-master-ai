from pathlib import Path

from PIL import Image, ImageEnhance, ImageFilter


class ImageEnhanceService:
    """
    Service untuk mempercantik dan meningkatkan kualitas foto.
    """

    ALLOWED_EXTENSIONS = {
        ".jpg",
        ".jpeg",
        ".png",
        ".webp",
    }

    def enhance(
        self,
        input_path: str,
        output_path: str,
        scale: int = 2,
        sharpness: float = 1.5,
        contrast: float = 1.1,
        color: float = 1.05,
    ) -> str:

        input_file = Path(input_path)
        output_file = Path(output_path)

        if not input_file.exists():
            raise FileNotFoundError(
                f"Input image not found: {input_path}"
            )

        if input_file.suffix.lower() not in self.ALLOWED_EXTENSIONS:
            raise ValueError(
                "Unsupported image format."
            )

        output_file.parent.mkdir(
            parents=True,
            exist_ok=True
        )

        with Image.open(input_file) as image:

            # Pastikan mode aman untuk diproses
            if image.mode not in ("RGB", "RGBA"):
                image = image.convert("RGB")

            # --------------------------------------------------
            # UPSCALE
            # --------------------------------------------------

            if scale > 1:
                width = image.width * scale
                height = image.height * scale

                image = image.resize(
                    (width, height),
                    Image.Resampling.LANCZOS
                )

            # --------------------------------------------------
            # NOISE REDUCTION RINGAN
            # --------------------------------------------------

            image = image.filter(
                ImageFilter.MedianFilter(size=3)
            )

            # --------------------------------------------------
            # SHARPEN
            # --------------------------------------------------

            image = ImageEnhance.Sharpness(
                image
            ).enhance(sharpness)

            # --------------------------------------------------
            # CONTRAST
            # --------------------------------------------------

            image = ImageEnhance.Contrast(
                image
            ).enhance(contrast)

            # --------------------------------------------------
            # COLOR
            # --------------------------------------------------

            image = ImageEnhance.Color(
                image
            ).enhance(color)

            # --------------------------------------------------
            # SAVE
            # --------------------------------------------------

            save_format = (
                "PNG"
                if output_file.suffix.lower() == ".png"
                else "JPEG"
            )

            if save_format == "JPEG" and image.mode == "RGBA":
                image = image.convert("RGB")

            image.save(
                output_file,
                format=save_format,
                quality=95,
                optimize=True
            )

        return str(output_file)
