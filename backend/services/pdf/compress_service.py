# ==========================================================
# PDF MASTER AI
# Compress PDF Service
# ==========================================================

# ----------------------------------------------------------
# IMPORT
# ----------------------------------------------------------

import os
import re
import shutil
import tempfile
from pathlib import Path

import fitz

from utils.file import get_file_size

from core.logger import info

from services.pdf.base_pdf_service import BasePdfService


# ----------------------------------------------------------
# COMPRESS SERVICE
# ----------------------------------------------------------

class CompressService(
    BasePdfService
):

    """
    PDF Compression Service.

    Compresses PDF structure and images
    to get as close as possible to target size.
    """

    def __init__(
        self,
        db
    ):

        super().__init__(db)

    # --------------------------------------------------
    # ANALYZE PDF COMPONENTS
    # --------------------------------------------------

    def analyze_pdf(
        self,
        input_path: str
    ) -> dict:

        """
        Analyze measurable PDF components.

        This method only reads the PDF.
        It does NOT modify the document.
        """

        document = fitz.open(
            input_path
        )

        try:

            # --------------------------------------------------
            # BASIC INFORMATION
            # --------------------------------------------------

            file_path = Path(
                input_path
            )

            file_size = (
                file_path.stat().st_size
            )

            page_count = len(
                document
            )

            xref_count = (
                document.xref_length()
            )

            # --------------------------------------------------
            # OBJECT TRACKING
            # --------------------------------------------------

            image_xrefs = set()

            font_xrefs = set()

            content_xrefs = set()

            # --------------------------------------------------
            # FIND PAGE OBJECTS
            # --------------------------------------------------

            for page in document:

                # --------------------------------------------------
                # IMAGES
                # --------------------------------------------------

                try:

                    images = page.get_images(
                        full=True
                    )

                except Exception:

                    images = []

                for image in images:

                    if not image:
                        continue

                    xref = image[0]

                    if xref > 0:

                        image_xrefs.add(
                            xref
                        )

                # --------------------------------------------------
                # FONTS
                # --------------------------------------------------

                try:

                    fonts = page.get_fonts(
                        full=True
                    )

                except Exception:

                    fonts = []

                for font in fonts:

                    if not font:
                        continue

                    xref = font[0]

                    if xref > 0:

                        font_xrefs.add(
                            xref
                        )

                # --------------------------------------------------
                # CONTENT STREAMS
                # --------------------------------------------------

                try:

                    contents = (
                        page.get_contents()
                    )

                except Exception:

                    contents = []

                for xref in contents:

                    if xref > 0:

                        content_xrefs.add(
                            xref
                        )

            # --------------------------------------------------
            # RAW STREAM SIZE
            # --------------------------------------------------

            def get_raw_stream_size(
                xref: int
            ) -> int:

                try:

                    raw_stream = (
                        document.xref_stream_raw(
                            xref
                        )
                    )

                    if raw_stream:

                        return len(
                            raw_stream
                        )

                except Exception:

                    pass

                return 0

            # --------------------------------------------------
            # IMAGE SIZE
            # --------------------------------------------------

            image_size = 0

            for xref in image_xrefs:

                image_size += (
                    get_raw_stream_size(
                        xref
                    )
                )

            # --------------------------------------------------
            # FONT SIZE
            # --------------------------------------------------

            font_size = 0

            for xref in font_xrefs:

                font_size += (
                    get_raw_stream_size(
                        xref
                    )
                )

            # --------------------------------------------------
            # CONTENT SIZE
            # --------------------------------------------------

            content_size = 0

            for xref in content_xrefs:

                content_size += (
                    get_raw_stream_size(
                        xref
                    )
                )

            # --------------------------------------------------
            # OTHER STREAMS
            # --------------------------------------------------

            excluded_xrefs = (
                image_xrefs
                | font_xrefs
                | content_xrefs
            )

            other_stream_size = 0

            other_stream_count = 0

            for xref in range(
                1,
                xref_count
            ):

                if xref in excluded_xrefs:

                    continue

                stream_size = (
                    get_raw_stream_size(
                        xref
                    )
                )

                if stream_size <= 0:

                    continue

                other_stream_size += (
                    stream_size
                )

                other_stream_count += 1

            # --------------------------------------------------
            # METADATA
            # --------------------------------------------------

            metadata_size = 0

            try:

                metadata = (
                    document.metadata
                )

                if metadata:

                    metadata_size = len(
                        str(
                            metadata
                        ).encode(
                            "utf-8"
                        )
                    )

            except Exception:

                metadata_size = 0

            # --------------------------------------------------
            # PERCENTAGE
            # --------------------------------------------------

            def percentage(
                value: int
            ) -> float:

                if file_size <= 0:

                    return 0.0

                return round(
                    (
                        value
                        / file_size
                    ) * 100,
                    2
                )

            # --------------------------------------------------
            # TOTAL
            # --------------------------------------------------

            measured_size = (
                image_size
                + font_size
                + content_size
                + other_stream_size
            )

            # --------------------------------------------------
            # RESULT
            # --------------------------------------------------

            return {

                "success": True,

                "file": {

                    "path": str(
                        file_path
                    ),

                    "size_bytes": (
                        file_size
                    ),

                    "size_kb": round(
                        file_size / 1024,
                        2
                    ),

                    "size_mb": round(
                        file_size / (
                            1024 * 1024
                        ),
                        2
                    )

                },

                "pages": page_count,

                "objects": {

                    "xref_count": (
                        xref_count
                    ),

                    "images": len(
                        image_xrefs
                    ),

                    "fonts": len(
                        font_xrefs
                    ),

                    "content_streams": len(
                        content_xrefs
                    ),

                    "other_streams": (
                        other_stream_count
                    )

                },

                "components": {

                    "images": {

                        "bytes": (
                            image_size
                        ),

                        "kb": round(
                            image_size / 1024,
                            2
                        ),

                        "mb": round(
                            image_size / (
                                1024 * 1024
                            ),
                            2
                        ),

                        "percentage": (
                            percentage(
                                image_size
                            )
                        )

                    },

                    "fonts": {

                        "bytes": (
                            font_size
                        ),

                        "kb": round(
                            font_size / 1024,
                            2
                        ),

                        "mb": round(
                            font_size / (
                                1024 * 1024
                            ),
                            2
                        ),

                        "percentage": (
                            percentage(
                                font_size
                            )
                        )

                    },

                    "content": {

                        "bytes": (
                            content_size
                        ),

                        "kb": round(
                            content_size / 1024,
                            2
                        ),

                        "mb": round(
                            content_size / (
                                1024 * 1024
                            ),
                            2
                        ),

                        "percentage": (
                            percentage(
                                content_size
                            )
                        )

                    },

                    "other": {

                        "bytes": (
                            other_stream_size
                        ),

                        "kb": round(
                            other_stream_size / 1024,
                            2
                        ),

                        "mb": round(
                            other_stream_size / (
                                1024 * 1024
                            ),
                            2
                        ),

                        "percentage": (
                            percentage(
                                other_stream_size
                            )
                        )

                    },

                    "metadata": {

                        "bytes": (
                            metadata_size
                        ),

                        "kb": round(
                            metadata_size / 1024,
                            2
                        ),

                        "percentage": (
                            percentage(
                                metadata_size
                            )
                        )

                    }

                },

                "measured_streams": {

                    "bytes": (
                        measured_size
                    ),

                    "kb": round(
                        measured_size / 1024,
                        2
                    ),

                    "mb": round(
                        measured_size / (
                            1024 * 1024
                        ),
                        2
                    )

                }

            }

        finally:

            document.close()


    # --------------------------------------------------
    # ANALYZE OTHER PDF OBJECTS
    # --------------------------------------------------

    def analyze_other_objects(
        self,
        input_path: str
    ) -> dict:

        """
        Analyze PDF objects that are not classified
        as normal image, font, or page content streams.

        This method only reads the PDF.
        It does NOT modify the document.
        """

        document = fitz.open(
            input_path
        )

        try:

            file_path = Path(
                input_path
            )

            file_size = (
                file_path.stat().st_size
            )

            xref_count = (
                document.xref_length()
            )

            # --------------------------------------------------
            # KNOWN OBJECTS
            # --------------------------------------------------

            image_xrefs = set()

            font_xrefs = set()

            content_xrefs = set()

            # --------------------------------------------------
            # COLLECT PAGE REFERENCES
            # --------------------------------------------------

            for page in document:

                # --------------------------------------------------
                # IMAGES
                # --------------------------------------------------

                try:

                    images = page.get_images(
                        full=True
                    )

                except Exception:

                    images = []

                for image in images:

                    if not image:
                        continue

                    xref = image[0]

                    if xref > 0:

                        image_xrefs.add(
                            xref
                        )

                # --------------------------------------------------
                # FONTS
                # --------------------------------------------------

                try:

                    fonts = page.get_fonts(
                        full=True
                    )

                except Exception:

                    fonts = []

                for font in fonts:

                    if not font:
                        continue

                    xref = font[0]

                    if xref > 0:

                        font_xrefs.add(
                            xref
                        )

                # --------------------------------------------------
                # CONTENT
                # --------------------------------------------------

                try:

                    contents = (
                        page.get_contents()
                    )

                except Exception:

                    contents = []

                for xref in contents:

                    if xref > 0:

                        content_xrefs.add(
                            xref
                        )

            # --------------------------------------------------
            # RAW STREAM HELPER
            # --------------------------------------------------

            def get_raw_stream(
                xref: int
            ):

                try:

                    return (
                        document.xref_stream_raw(
                            xref
                        )
                    )

                except Exception:

                    return None

            # --------------------------------------------------
            # OBJECT TYPE HELPER
            # --------------------------------------------------

            def get_key(
                xref: int,
                key: str
            ) -> str:

                try:

                    value = (
                        document.xref_get_key(
                            xref,
                            key
                        )
                    )

                    if (
                        value
                        and len(value) > 1
                        and value[1]
                    ):

                        return str(
                            value[1]
                        )

                except Exception:

                    pass

                return ""

            # --------------------------------------------------
            # CATEGORIES
            # --------------------------------------------------

            categories = {

                "image_related": set(),

                "form_xobject": set(),

                "font_related": set(),

                "xobject": set(),

                "pattern": set(),

                "shading": set(),

                "graphics_state": set(),

                "color_space": set(),

                "embedded_file": set(),

                "metadata": set(),

                "object_stream": set(),

                "unknown": set()

            }

            # --------------------------------------------------
            # SCAN OBJECTS
            # --------------------------------------------------

            excluded_xrefs = (
                image_xrefs
                | font_xrefs
                | content_xrefs
            )

            for xref in range(
                1,
                xref_count
            ):

                if xref in excluded_xrefs:

                    continue

                raw_stream = (
                    get_raw_stream(
                        xref
                    )
                )

                stream_size = (
                    len(raw_stream)
                    if raw_stream
                    else 0
                )

                type_name = get_key(
                    xref,
                    "Type"
                )

                subtype_name = get_key(
                    xref,
                    "Subtype"
                )

                category = "unknown"

                # --------------------------------------------------
                # IMAGE RELATED
                # --------------------------------------------------

                if (
                    subtype_name
                    == "/Image"
                ):

                    category = (
                        "image_related"
                    )

                # --------------------------------------------------
                # FORM XOBJECT
                # --------------------------------------------------

                elif (
                    subtype_name
                    == "/Form"
                ):

                    category = (
                        "form_xobject"
                    )

                # --------------------------------------------------
                # FONT
                # --------------------------------------------------

                elif (
                    type_name
                    == "/Font"
                    or subtype_name
                    in {
                        "/Type1",
                        "/TrueType",
                        "/Type0",
                        "/CIDFontType0",
                        "/CIDFontType2"
                    }
                ):

                    category = (
                        "font_related"
                    )

                # --------------------------------------------------
                # XOBJECT
                # --------------------------------------------------

                elif (
                    type_name
                    == "/XObject"
                ):

                    category = (
                        "xobject"
                    )

                # --------------------------------------------------
                # PATTERN
                # --------------------------------------------------

                elif (
                    type_name
                    == "/Pattern"
                ):

                    category = (
                        "pattern"
                    )

                # --------------------------------------------------
                # SHADING
                # --------------------------------------------------

                elif (
                    type_name
                    == "/Shading"
                ):

                    category = (
                        "shading"
                    )

                # --------------------------------------------------
                # GRAPHICS STATE
                # --------------------------------------------------

                elif (
                    type_name
                    == "/ExtGState"
                ):

                    category = (
                        "graphics_state"
                    )

                # --------------------------------------------------
                # COLOR SPACE
                # --------------------------------------------------

                elif (
                    type_name
                    == "/ColorSpace"
                ):

                    category = (
                        "color_space"
                    )

                # --------------------------------------------------
                # EMBEDDED FILE
                # --------------------------------------------------

                elif (
                    type_name
                    == "/Filespec"
                ):

                    category = (
                        "embedded_file"
                    )

                # --------------------------------------------------
                # METADATA
                # --------------------------------------------------

                elif (
                    type_name
                    == "/Metadata"
                ):

                    category = (
                        "metadata"
                    )

                # --------------------------------------------------
                # OBJECT STREAM
                # --------------------------------------------------

                elif (
                    type_name
                    == "/ObjStm"
                ):

                    category = (
                        "object_stream"
                    )

                categories[
                    category
                ].add(
                    (
                        xref,
                        stream_size
                    )
                )

            # --------------------------------------------------
            # BUILD RESULT
            # --------------------------------------------------

            components = {}

            for category, objects in (
                categories.items()
            ):

                total_size = sum(
                    size
                    for _, size
                    in objects
                )

                components[
                    category
                ] = {

                    "objects": len(
                        objects
                    ),

                    "bytes": total_size,

                    "kb": round(
                        total_size / 1024,
                        2
                    ),

                    "mb": round(
                        total_size / (
                            1024 * 1024
                        ),
                        2
                    ),

                    "percentage": (
                        round(
                            (
                                total_size
                                / file_size
                            ) * 100,
                            2
                        )
                        if file_size > 0
                        else 0.0
                    )

                }

            # --------------------------------------------------
            # TOTAL
            # --------------------------------------------------

            total_other_bytes = sum(
                item["bytes"]
                for item in components.values()
            )

            return {

                "success": True,

                "file": {

                    "path": str(
                        file_path
                    ),

                    "size_bytes": (
                        file_size
                    ),

                    "size_kb": round(
                        file_size / 1024,
                        2
                    ),

                    "size_mb": round(
                        file_size / (
                            1024 * 1024
                        ),
                        2
                    )

                },

                "objects": {

                    "xref_count": (
                        xref_count
                    ),

                    "other_objects": sum(
                        item["objects"]
                        for item in (
                            components.values()
                        )
                    )

                },

                "components": components,

                "total_other_streams": {

                    "bytes": (
                        total_other_bytes
                    ),

                    "kb": round(
                        total_other_bytes / 1024,
                        2
                    ),

                    "mb": round(
                        total_other_bytes / (
                            1024 * 1024
                        ),
                        2
                    )

                }

            }

        finally:

            document.close()

    # --------------------------------------------------
    # ANALYZE LARGEST UNKNOWN OBJECTS
    # --------------------------------------------------

    def analyze_unknown_objects(
        self,
        input_path: str,
        limit: int = 20
    ) -> dict:

        """
        Find the largest unknown PDF objects.

        This method only reads the PDF.
        It does NOT modify the document.
        """

        document = fitz.open(
            input_path
        )

        try:

            file_path = Path(
                input_path
            )

            file_size = (
                file_path.stat().st_size
            )

            xref_count = (
                document.xref_length()
            )

            # --------------------------------------------------
            # KNOWN OBJECTS
            # --------------------------------------------------

            image_xrefs = set()

            font_xrefs = set()

            content_xrefs = set()

            for page in document:

                # --------------------------------------------------
                # IMAGES
                # --------------------------------------------------

                try:

                    images = page.get_images(
                        full=True
                    )

                except Exception:

                    images = []

                for image in images:

                    if image:

                        xref = image[0]

                        if xref > 0:

                            image_xrefs.add(
                                xref
                            )

                # --------------------------------------------------
                # FONTS
                # --------------------------------------------------

                try:

                    fonts = page.get_fonts(
                        full=True
                    )

                except Exception:

                    fonts = []

                for font in fonts:

                    if font:

                        xref = font[0]

                        if xref > 0:

                            font_xrefs.add(
                                xref
                            )

                # --------------------------------------------------
                # CONTENT
                # --------------------------------------------------

                try:

                    contents = (
                        page.get_contents()
                    )

                except Exception:

                    contents = []

                for xref in contents:

                    if xref > 0:

                        content_xrefs.add(
                            xref
                        )

            # --------------------------------------------------
            # EXCLUDED OBJECTS
            # --------------------------------------------------

            excluded_xrefs = (
                image_xrefs
                | font_xrefs
                | content_xrefs
            )

            # --------------------------------------------------
            # FIND UNKNOWN OBJECTS
            # --------------------------------------------------

            unknown_objects = []

            for xref in range(
                1,
                xref_count
            ):

                if xref in excluded_xrefs:

                    continue

                # --------------------------------------------------
                # RAW STREAM
                # --------------------------------------------------

                try:

                    raw_stream = (
                        document.xref_stream_raw(
                            xref
                        )
                    )

                except Exception:

                    raw_stream = None

                stream_size = (
                    len(raw_stream)
                    if raw_stream
                    else 0
                )

                # --------------------------------------------------
                # OBJECT TYPE
                # --------------------------------------------------

                try:

                    type_result = (
                        document.xref_get_key(
                            xref,
                            "Type"
                        )
                    )

                except Exception:

                    type_result = (
                        None,
                        None
                    )

                try:

                    subtype_result = (
                        document.xref_get_key(
                            xref,
                            "Subtype"
                        )
                    )

                except Exception:

                    subtype_result = (
                        None,
                        None
                    )

                type_name = (
                    str(
                        type_result[1]
                    )
                    if (
                        type_result
                        and len(type_result) > 1
                        and type_result[1]
                    )
                    else ""
                )

                subtype_name = (
                    str(
                        subtype_result[1]
                    )
                    if (
                        subtype_result
                        and len(subtype_result) > 1
                        and subtype_result[1]
                    )
                    else ""
                )

                # --------------------------------------------------
                # UNKNOWN CHECK
                # --------------------------------------------------

                known = False

                if subtype_name in {

                    "/Image",
                    "/Form",
                    "/Type1",
                    "/TrueType",
                    "/Type0",
                    "/CIDFontType0",
                    "/CIDFontType2"

                }:

                    known = True

                if type_name in {

                    "/Font",
                    "/XObject",
                    "/Pattern",
                    "/Shading",
                    "/ExtGState",
                    "/ColorSpace",
                    "/Filespec",
                    "/Metadata",
                    "/ObjStm"

                }:

                    known = True

                if known:

                    continue

                # --------------------------------------------------
                # OBJECT SOURCE
                # --------------------------------------------------

                try:

                    object_source = (
                        document.xref_object(
                            xref,
                            compressed=False
                        )
                    )

                except Exception:

                    object_source = ""

                # --------------------------------------------------
                # ADD OBJECT
                # --------------------------------------------------

                unknown_objects.append({

                    "xref": xref,

                    "bytes": stream_size,

                    "kb": round(
                        stream_size / 1024,
                        2
                    ),

                    "mb": round(
                        stream_size / (
                            1024 * 1024
                        ),
                        4
                    ),

                    "type": type_name,

                    "subtype": subtype_name,

                    "object_preview": (
                        object_source[:300]
                        if object_source
                        else ""
                    )

                })

            # --------------------------------------------------
            # SORT BY SIZE
            # --------------------------------------------------

            unknown_objects.sort(
                key=lambda item: item[
                    "bytes"
                ],
                reverse=True
            )

            # --------------------------------------------------
            # TOP OBJECTS
            # --------------------------------------------------

            largest_objects = (
                unknown_objects[:limit]
            )

            # --------------------------------------------------
            # TOTAL UNKNOWN SIZE
            # --------------------------------------------------

            total_unknown_bytes = sum(
                item["bytes"]
                for item in unknown_objects
            )

            # --------------------------------------------------
            # RESULT
            # --------------------------------------------------

            return {

                "success": True,

                "file": {

                    "path": str(
                        file_path
                    ),

                    "size_bytes": (
                        file_size
                    ),

                    "size_mb": round(
                        file_size / (
                            1024 * 1024
                        ),
                        2
                    )

                },

                "objects": {

                    "xref_count": (
                        xref_count
                    ),

                    "unknown_count": (
                        len(
                            unknown_objects
                        )
                    ),

                    "unknown_size_bytes": (
                        total_unknown_bytes
                    ),

                    "unknown_size_mb": round(
                        total_unknown_bytes / (
                            1024 * 1024
                        ),
                        2
                    )

                },

                "largest_unknown": (
                    largest_objects
                )

            }

        finally:

            document.close()

    # --------------------------------------------------
    # ANALYZE IMAGE RELATED OBJECTS
    # --------------------------------------------------

    def analyze_image_related(
        self,
        input_path: str,
        limit: int = 30
    ) -> dict:

        """
        Analyze image-related PDF objects.

        This method only reads the PDF.
        It does NOT modify the document.
        """

        document = fitz.open(
            input_path
        )

        try:

            file_path = Path(
                input_path
            )

            file_size = (
                file_path.stat().st_size
            )

            xref_count = (
                document.xref_length()
            )

            # --------------------------------------------------
            # COLLECT IMAGE REFERENCES
            # --------------------------------------------------

            image_objects = {}

            for page_number, page in enumerate(
                document
            ):

                try:

                    images = page.get_images(
                        full=True
                    )

                except Exception:

                    images = []

                for image in images:

                    if not image:
                        continue

                    xref = image[0]

                    if xref <= 0:
                        continue

                    smask = (
                        image[1]
                        if len(image) > 1
                        else 0
                    )

                    mask = (
                        image[2]
                        if len(image) > 2
                        else 0
                    )

                    width = (
                        image[2]
                        if len(image) > 2
                        else 0
                    )

                    height = (
                        image[3]
                        if len(image) > 3
                        else 0
                    )

                    colorspace = (
                        image[4]
                        if len(image) > 4
                        else 0
                    )

                    bpc = (
                        image[5]
                        if len(image) > 5
                        else 0
                    )

                    image_objects[
                        xref
                    ] = {

                        "xref": xref,

                        "smask": smask,

                        "mask": mask,

                        "width": width,

                        "height": height,

                        "colorspace": colorspace,

                        "bpc": bpc,

                        "pages": set()

                    }

                    image_objects[
                        xref
                    ][
                        "pages"
                    ].add(
                        page_number + 1
                    )

            # --------------------------------------------------
            # RAW STREAM SIZE
            # --------------------------------------------------

            def raw_size(
                xref: int
            ) -> int:

                try:

                    data = (
                        document.xref_stream_raw(
                            xref
                        )
                    )

                    if data:

                        return len(
                            data
                        )

                except Exception:

                    pass

                return 0

            # --------------------------------------------------
            # ANALYZE IMAGE OBJECTS
            # --------------------------------------------------

            normal_images = []

            smask_objects = []

            mask_objects = []

            total_image_bytes = 0

            total_smask_bytes = 0

            total_mask_bytes = 0

            processed_smask = set()

            processed_mask = set()

            for xref, data in (
                image_objects.items()
            ):

                image_bytes = raw_size(
                    xref
                )

                total_image_bytes += (
                    image_bytes
                )

                normal_images.append({

                    "xref": xref,

                    "bytes": image_bytes,

                    "kb": round(
                        image_bytes / 1024,
                        2
                    ),

                    "mb": round(
                        image_bytes / (
                            1024 * 1024
                        ),
                        4
                    ),

                    "width": data[
                        "width"
                    ],

                    "height": data[
                        "height"
                    ],

                    "colorspace": data[
                        "colorspace"
                    ],

                    "bpc": data[
                        "bpc"
                    ],

                    "smask": data[
                        "smask"
                    ],

                    "mask": data[
                        "mask"
                    ],

                    "pages": sorted(
                        data[
                            "pages"
                        ]
                    )

                })

                # --------------------------------------------------
                # SMASK
                # --------------------------------------------------

                smask = data[
                    "smask"
                ]

                if smask > 0:

                    if smask not in (
                        processed_smask
                    ):

                        processed_smask.add(
                            smask
                        )

                        size = raw_size(
                            smask
                        )

                        total_smask_bytes += (
                            size
                        )

                        smask_objects.append({

                            "xref": smask,

                            "parent_image": xref,

                            "bytes": size,

                            "kb": round(
                                size / 1024,
                                2
                            ),

                            "mb": round(
                                size / (
                                    1024 * 1024
                                ),
                                4
                            )

                        })

                # --------------------------------------------------
                # MASK
                # --------------------------------------------------

                mask = data[
                    "mask"
                ]

                if mask > 0:

                    if mask not in (
                        processed_mask
                    ):

                        processed_mask.add(
                            mask
                        )

                        size = raw_size(
                            mask
                        )

                        total_mask_bytes += (
                            size
                        )

                        mask_objects.append({

                            "xref": mask,

                            "parent_image": xref,

                            "bytes": size,

                            "kb": round(
                                size / 1024,
                                2
                            ),

                            "mb": round(
                                size / (
                                    1024 * 1024
                                ),
                                4
                            )

                        })

            # --------------------------------------------------
            # SORT
            # --------------------------------------------------

            normal_images.sort(
                key=lambda item: item[
                    "bytes"
                ],
                reverse=True
            )

            smask_objects.sort(
                key=lambda item: item[
                    "bytes"
                ],
                reverse=True
            )

            mask_objects.sort(
                key=lambda item: item[
                    "bytes"
                ],
                reverse=True
            )

            # --------------------------------------------------
            # RESULT
            # --------------------------------------------------

            return {

                "success": True,

                "file": {

                    "path": str(
                        file_path
                    ),

                    "size_bytes": (
                        file_size
                    ),

                    "size_mb": round(
                        file_size / (
                            1024 * 1024
                        ),
                        2
                    )

                },

                "objects": {

                    "xref_count": (
                        xref_count
                    ),

                    "images": len(
                        normal_images
                    ),

                    "smasks": len(
                        smask_objects
                    ),

                    "masks": len(
                        mask_objects
                    )

                },

                "totals": {

                    "images_bytes": (
                        total_image_bytes
                    ),

                    "images_mb": round(
                        total_image_bytes / (
                            1024 * 1024
                        ),
                        2
                    ),

                    "smask_bytes": (
                        total_smask_bytes
                    ),

                    "smask_mb": round(
                        total_smask_bytes / (
                            1024 * 1024
                        ),
                        2
                    ),

                    "mask_bytes": (
                        total_mask_bytes
                    ),

                    "mask_mb": round(
                        total_mask_bytes / (
                            1024 * 1024
                        ),
                        2
                    )

                },

                "largest_images": (
                    normal_images[
                        :limit
                    ]
                ),

                "largest_smask": (
                    smask_objects[
                        :limit
                    ]
                ),

                "largest_mask": (
                    mask_objects[
                        :limit
                    ]
                )

            }

        finally:

            document.close()

# ------------------------------------------------------
# COMPRESS IMAGES
# ------------------------------------------------------

    def _compress_images(
        self,
        input_path: str,
        output_path: str,
        quality: int = 70,
        shrink_factor: int = 1
    ) -> str:
        document = fitz.open(input_path)
        processed_xrefs = set()
        try:
            for page in document:
                image_list = page.get_images(full=True)
                for img_info in image_list:
                    xref = img_info[0]
                    if xref in processed_xrefs:
                        continue
                    processed_xrefs.add(xref)

                    try:
                        pix = fitz.Pixmap(document, xref)
                        if pix.n >= 5 or pix.alpha:
                            pix = fitz.Pixmap(fitz.csRGB, pix)

                        img_data = pix.tobytes("jpg")
                        img = Image.open(io.BytesIO(img_data))

                        if shrink_factor > 1:
                            new_size = (max(1, img.width // shrink_factor), max(1, img.height // shrink_factor))
                            img = img.resize(new_size, Image.Resampling.BILINEAR)

                        buffer = io.BytesIO()
                        img.save(buffer, format="JPEG", quality=quality)
                        page.replace_image(xref, stream=buffer.getvalue())
                    except Exception:
                        continue

            document.save(
                output_path,
                garbage=4,
                deflate=True,
                deflate_images=True,
                deflate_fonts=True
            )
            document.close()
            return output_path
        except Exception:
            document.close()
            return input_path
    def _compress_once(
        self,
        input_path: str,
        output_path: str,
        quality: int,
        shrink_factor: int = 1
    ) -> str:

        """Perform one image compression pass."""

        return self._compress_images(
            input_path,
            output_path,
            quality,
            shrink_factor
        )

        # ------------------------------------------------------
    # COMPRESS
    # ------------------------------------------------------

    # ------------------------------------------------------
    # COMPRESS
    # ------------------------------------------------------

    # ------------------------------------------------------
    # EXTREME COMPRESSION ENGINE
    # ------------------------------------------------------

    def _extreme_compress(
        self,
        input_path: str,
        output_path: str,
        dpi: int = 40,
        quality: int = 35
    ) -> str:

        """
        Extreme fallback compression.

        Setiap halaman dirender menjadi JPEG.
        Digunakan hanya ketika compression engine
        normal belum mencapai target.
        """

        source = fitz.open(
            input_path
        )

        result = fitz.open()

        try:

            scale = dpi / 72.0

            matrix = fitz.Matrix(
                scale,
                scale
            )

            for page in source:

                pix = page.get_pixmap(
                    matrix=matrix,
                    alpha=False
                )

                jpeg_bytes = pix.tobytes(
                    "jpeg",
                    jpg_quality=quality
                )

                rect = fitz.Rect(
                    0,
                    0,
                    pix.width,
                    pix.height
                )

                new_page = result.new_page(
                    width=rect.width,
                    height=rect.height
                )

                new_page.insert_image(
                    rect,
                    stream=jpeg_bytes
                )

            result.save(
                output_path,
                garbage=4,
                deflate=True,
                clean=True
            )

        finally:

            result.close()
            source.close()

        return output_path

    def compress(
        self,
        input_path: str,
        output_path: str,
        target_size_kb: int
    ) -> str:

        """
        Progressive PDF compression.

        Profiles:
        - LARGE  : > 10 MB
        - MEDIUM : > 1 MB and <= 10 MB
        - SMALL  : <= 1 MB

        Minimum target:
        100 KB
        """

        # --------------------------------------------------
        # MINIMUM TARGET
        # --------------------------------------------------

        minimum_target_kb = 100

        target_size_kb = max(
            int(target_size_kb),
            minimum_target_kb
        )

        target_bytes = (
            target_size_kb * 1024
        )

        # --------------------------------------------------
        # ORIGINAL SIZE
        # --------------------------------------------------

        original_size = get_file_size(
            input_path
        )

        original_size_kb = (
            original_size / 1024
        )

        original_size_mb = (
            original_size / (
                1024 * 1024
            )
        )

        # --------------------------------------------------
        # ALREADY SMALL ENOUGH
        # --------------------------------------------------

        if original_size <= target_bytes:

            shutil.copy2(
                input_path,
                output_path
            )

            info(
                "PDF already below target: "
                f"{original_size} bytes <= "
                f"{target_bytes} bytes"
            )

            return output_path

        # --------------------------------------------------
        # SELECT PROFILE
        # --------------------------------------------------

        if original_size_mb > 10:

            compression_profile = "LARGE"

        elif original_size_kb > 1024:

            compression_profile = "MEDIUM"

        else:

            compression_profile = "SMALL"

        info(
            "Compression profile: "
            f"{compression_profile} | "
            f"original={original_size} bytes | "
            f"target={target_bytes} bytes"
        )

        # --------------------------------------------------
        # LARGE PROFILE
        # --------------------------------------------------

        large_levels = [
            {"quality": 85, "shrink": 1},
            {"quality": 75, "shrink": 1},
            {"quality": 65, "shrink": 2},
            {"quality": 60, "shrink": 2}
        ]

        medium_levels = [
            {"quality": 80, "shrink": 1},
            {"quality": 70, "shrink": 1},
            {"quality": 60, "shrink": 2}
        ]

        small_levels = [
            {"quality": 75, "shrink": 1},
            {"quality": 65, "shrink": 1},
            {"quality": 60, "shrink": 1}
        ]

        # --------------------------------------------------
        # SELECT LEVELS
        # --------------------------------------------------

        if compression_profile == "LARGE":

            compression_levels = large_levels

        elif compression_profile == "MEDIUM":

            compression_levels = medium_levels

        else:

            compression_levels = small_levels

        # --------------------------------------------------
        # TEMPORARY DIRECTORY
        # --------------------------------------------------

        temp_directory = tempfile.mkdtemp(
            prefix="pdf_progressive_"
        )

        current_path = input_path
        current_size = original_size

        best_path = input_path
        best_size = original_size

        try:

            # --------------------------------------------------
            # PROGRESSIVE COMPRESSION
            # --------------------------------------------------

            for index, settings in enumerate(
                compression_levels,
                start=1
            ):

                quality = settings[
                    "quality"
                ]

                shrink_factor = settings[
                    "shrink"
                ]

                attempt_path = os.path.join(
                    temp_directory,
                    f"level_{index}.pdf"
                )

                info(
                    "Progressive compression "
                    f"{index}/{len(compression_levels)} | "
                    f"profile={compression_profile} | "
                    f"quality={quality} | "
                    f"shrink={shrink_factor} | "
                    f"input={current_size} bytes"
                )

                # --------------------------------------------------
                # COMPRESS CURRENT VERSION
                # --------------------------------------------------

                try:

                    self._compress_once(
                        current_path,
                        attempt_path,
                        quality,
                        shrink_factor
                    )

                except Exception as exc:

                    info(
                        "Compression level failed: "
                        f"{index} | "
                        f"error={exc}"
                    )

                    continue

                # --------------------------------------------------
                # CHECK OUTPUT
                # --------------------------------------------------

                if not os.path.isfile(
                    attempt_path
                ):

                    info(
                        "Compression output missing: "
                        f"level={index}"
                    )

                    continue

                compressed_size = get_file_size(
                    attempt_path
                )

                # --------------------------------------------------
                # NEVER ACCEPT LARGER RESULT
                # --------------------------------------------------

                if compressed_size >= current_size:

                    info(
                        "Compression level did not reduce size: "
                        f"{current_size} -> "
                        f"{compressed_size} bytes"
                    )

                    continue

                # --------------------------------------------------
                # ACCEPT NEW VERSION
                # --------------------------------------------------

                current_path = attempt_path
                current_size = compressed_size

                best_path = attempt_path
                best_size = compressed_size

                info(
                    "Progressive compression result: "
                    f"{original_size} -> "
                    f"{best_size} bytes"
                )

                # --------------------------------------------------
                # TARGET REACHED
                # --------------------------------------------------

                if best_size <= target_bytes:

                    info(
                        "Target size reached: "
                        f"{best_size} <= "
                        f"{target_bytes} bytes"
                    )

                    break

                # --------------------------------------------------
                # HARD MINIMUM 100 KB
                # --------------------------------------------------

                if best_size <= (
                    minimum_target_kb * 1024
                ):

                    info(
                        "Minimum compression size reached: "
                        f"{best_size} bytes"
                    )

                    break

            # --------------------------------------------------
            # EXTREME ENGINE FALLBACK
            # --------------------------------------------------

            if best_size > target_bytes:

                info(
                    "Normal compression did not reach target. "
                    "Starting Extreme Engine."
                )

                extreme_profiles = [
                    {"dpi": 72, "quality": 50},
                    {"dpi": 60, "quality": 50},
                    {"dpi": 50, "quality": 40},
                    {"dpi": 40, "quality": 35},
                    {"dpi": 40, "quality": 25}
                ]

                for extreme_index, profile in enumerate(
                    extreme_profiles,
                    start=1
                ):

                    extreme_dpi = profile[
                        "dpi"
                    ]

                    extreme_quality = profile[
                        "quality"
                    ]

                    extreme_path = os.path.join(
                        temp_directory,
                        (
                            f"extreme_"
                            f"{extreme_dpi}dpi_"
                            f"q{extreme_quality}.pdf"
                        )
                    )

                    info(
                        "Extreme compression "
                        f"{extreme_index}/"
                        f"{len(extreme_profiles)} | "
                        f"dpi={extreme_dpi} | "
                        f"quality={extreme_quality}"
                    )

                    try:

                        self._extreme_compress(
                            input_path,
                            extreme_path,
                            dpi=extreme_dpi,
                            quality=extreme_quality
                        )

                    except Exception as exc:

                        info(
                            "Extreme compression failed: "
                            f"dpi={extreme_dpi} | "
                            f"quality={extreme_quality} | "
                            f"error={exc}"
                        )

                        continue

                    if not os.path.isfile(
                        extreme_path
                    ):

                        continue

                    extreme_size = get_file_size(
                        extreme_path
                    )

                    info(
                        "Extreme result: "
                        f"{extreme_size} bytes | "
                        f"dpi={extreme_dpi} | "
                        f"quality={extreme_quality}"
                    )

                    if extreme_size < best_size:

                        best_path = extreme_path
                        best_size = extreme_size

                    if extreme_size <= target_bytes:

                        info(
                            "Extreme target reached: "
                            f"{extreme_size} <= "
                            f"{target_bytes} bytes"
                        )

                        break

            # --------------------------------------------------
            # COPY BEST RESULT
            # --------------------------------------------------

            shutil.copy2(
                best_path,
                output_path
            )

            info(
                "PDF progressive compression completed: "
                f"profile={compression_profile} | "
                f"{original_size} -> "
                f"{best_size} bytes"
            )

            return output_path

        finally:

            # --------------------------------------------------
            # CLEAN TEMPORARY DIRECTORY
            # --------------------------------------------------

            try:

                shutil.rmtree(
                    temp_directory,
                    ignore_errors=True
                )

            except Exception as exc:

                info(
                    "Failed to clean compression "
                    f"temporary directory: {exc}"
                )

    # ------------------------------------------------------
    # EXECUTE
    # ------------------------------------------------------

    def execute(
        self,
        file_id: int,
        output_path: str,
        target_size_kb: int
    ) -> dict:

        """
        Execute progressive PDF compression.

        Compression chain:

            original.pdf
                ↓
            level_1.pdf
                ↓
            level_2.pdf
                ↓
            level_3.pdf
                ↓
                ...

        The latest compressed level becomes
        the input for the next execution.
        """

        # --------------------------------------------------
        # GET FILE
        # --------------------------------------------------

        file = self.get_file(
            file_id
        )

        self.validate_pdf(
            file
        )

        # --------------------------------------------------
        # ORIGINAL FILE
        # --------------------------------------------------

        original_path = file.storage_path

        original_path_obj = Path(
            original_path
        )

        # --------------------------------------------------
        # COMPRESSION DIRECTORY
        # --------------------------------------------------

        compression_directory = Path(
            output_path
        ).parent

        compression_directory.mkdir(
            parents=True,
            exist_ok=True
        )

        # --------------------------------------------------
        # ORIGINAL BASE NAME
        # --------------------------------------------------

        original_name = (
            original_path_obj.stem
        )

        # --------------------------------------------------
        # TARGET NAME
        # --------------------------------------------------

        target_name = (
            Path(output_path).stem
        )

        # --------------------------------------------------
        # REMOVE EXISTING LEVEL SUFFIX
        #
        # Example:
        #
        # file_compressed_500kb_level_1
        #
        # becomes:
        #
        # file_compressed_500kb
        # --------------------------------------------------

        base_target_name = re.sub(
            r"_level_\d+$",
            "",
            target_name
        )

        # --------------------------------------------------
        # FIND PREVIOUS COMPRESSION LEVELS
        # --------------------------------------------------

        search_pattern = (
            f"{base_target_name}_level_*.pdf"
        )

        previous_files = list(
            compression_directory.glob(
                search_pattern
            )
        )

        # --------------------------------------------------
        # DETERMINE INPUT FILE
        # --------------------------------------------------

        if previous_files:

            # ----------------------------------------------
            # FIND HIGHEST LEVEL
            # ----------------------------------------------

            level_files = []

            for candidate in previous_files:

                match = re.search(
                    r"_level_(\d+)\.pdf$",
                    candidate.name,
                    re.IGNORECASE
                )

                if not match:
                    continue

                level_number = int(
                    match.group(1)
                )

                level_files.append(
                    (
                        level_number,
                        candidate
                    )
                )

            if level_files:

                level_files.sort(
                    key=lambda item: item[0]
                )

                current_level = (
                    level_files[-1][0]
                )

                input_path = str(
                    level_files[-1][1]
                )

                info(
                    "Previous compression level found: "
                    f"level={current_level} | "
                    f"input={input_path}"
                )

            else:

                current_level = 0

                input_path = (
                    original_path
                )

                info(
                    "No valid previous compression level. "
                    f"Using original PDF: {input_path}"
                )

        else:

            current_level = 0

            input_path = (
                original_path
            )

            info(
                "First compression execution. "
                f"Using original PDF: {input_path}"
            )

        # --------------------------------------------------
        # NEXT LEVEL
        # --------------------------------------------------

        next_level = (
            current_level + 1
        )

        # --------------------------------------------------
        # OUTPUT FILE
        # --------------------------------------------------

        output_file = (
            f"{base_target_name}"
            f"_level_{next_level}.pdf"
        )

        final_output_path = str(
            compression_directory
            / output_file
        )

        # --------------------------------------------------
        # BEFORE SIZE
        # --------------------------------------------------

        before_size = get_file_size(
            input_path
        )

        # --------------------------------------------------
        # LOG INPUT
        # --------------------------------------------------

        info(
            "Executing PDF compression: "
            f"level={next_level} | "
            f"input={input_path} | "
            f"input_size={before_size} | "
            f"target={target_size_kb}KB"
        )

        # --------------------------------------------------
        # COMPRESS
        # --------------------------------------------------

        result = self.compress(
            input_path,
            final_output_path,
            target_size_kb
        )

        # --------------------------------------------------
        # AFTER SIZE
        # --------------------------------------------------

        after_size = get_file_size(
            result
        )

        # --------------------------------------------------
        # SAVE HISTORY
        # --------------------------------------------------

        self.save_history(
            file.user_id,
            file.id,
            "compress_pdf"
        )

        # --------------------------------------------------
        # LOG
        # --------------------------------------------------

        self.log(
            f"Compressed PDF: "
            f"{file.original_name} | "
            f"target={target_size_kb}KB | "
            f"before={before_size} | "
            f"after={after_size} | "
            f"level={next_level}"
        )

        # --------------------------------------------------
        # RESULT
        # --------------------------------------------------

        return {

            "input": input_path,

            "output": result,

            "before_size": before_size,

            "after_size": after_size,

            "saved_bytes": max(
                0,
                before_size - after_size
            ),

            "target_size_kb": target_size_kb,

            "compression_level": next_level

        }


