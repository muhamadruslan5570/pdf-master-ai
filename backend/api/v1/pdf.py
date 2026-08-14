from typing import Optional
# ==========================================================
# PDF MASTER AI
# PDF API
# ==========================================================

# ----------------------------------------------------------
# IMPORT
# ----------------------------------------------------------

from fastapi import APIRouter
from fastapi import Depends
from fastapi import Query
from fastapi import HTTPException

from fastapi.responses import FileResponse

from sqlalchemy.orm import Session

from models.file import File
from repositories.file_repository import FileRepository

from dependencies.database import get_db

from dependencies.current_user import (
    get_current_active_user
)

from services.pdf.compress_service import CompressService
from services.pdf.merge_service import MergeService
from services.pdf.split_service import SplitService
from services.pdf.rotate_service import RotateService
from services.pdf.watermark_service import WatermarkService
from services.pdf.protect_service import ProtectService
from services.pdf.unlock_service import UnlockService
from services.pdf.metadata_service import MetadataService
from services.pdf.thumbnail_service import ThumbnailService
from services.pdf.extract_service import ExtractService

from pathlib import Path

from services.pdf.pdf_to_jpg.service import PdfToJpgService
from services.pdf.pdf_to_word.service import PdfToWordService
from uuid import uuid4


# ----------------------------------------------------------
# ROUTER
# ----------------------------------------------------------

router = APIRouter()


# ==========================================================
# COMPRESS PDF
# ==========================================================

@router.post(
    "/compress",
    summary="Compress PDF",
    description="Compress PDF to target size."
)
def compress_pdf(
    file_id: int = Query(
        ...,
        gt=0,
        description="ID file PDF"
    ),

    target_size_kb: int = Query(
        ...,
        gt=0,
        description="Target ukuran PDF dalam KB"
    ),

    db: Session = Depends(
        get_db
    ),

    current_user=Depends(
        get_current_active_user
    )
):

    # ------------------------------------------------------
    # SERVICE
    # ------------------------------------------------------

    service = CompressService(
        db
    )

    # ------------------------------------------------------
    # GET FILE
    # ------------------------------------------------------

    file = service.get_file(
        file_id
    )

    # ------------------------------------------------------
    # CHECK USER
    # ------------------------------------------------------

    if file.user_id != current_user.id:

        raise HTTPException(
            status_code=403,
            detail="You do not have permission to access this file."
        )

    # ------------------------------------------------------
    # VALIDATE PDF
    # ------------------------------------------------------

    service.validate_pdf(
        file
    )

    # ------------------------------------------------------
    # OUTPUT DIRECTORY
    # ------------------------------------------------------

    input_path = Path(
        file.storage_path
    )

    output_directory = (
        input_path.parent /
        "compressed"
    )

    output_directory.mkdir(
        parents=True,
        exist_ok=True
    )

    # ------------------------------------------------------
    # OUTPUT FILE
    # ------------------------------------------------------

    output_filename = (
        f"{input_path.stem}_"
        f"compressed_"
        f"{target_size_kb}kb.pdf"
    )

    output_path = (
        output_directory /
        output_filename
    )

    # ------------------------------------------------------
    # COMPRESS
    # ------------------------------------------------------

    result = service.execute(
        file_id=file_id,
        output_path=str(
            output_path
        ),
        target_size_kb=target_size_kb
    )

# ------------------------------------------------------
# RESPONSE
# ------------------------------------------------------
    # ------------------------------------------------------

    return {

        "success": True,

        "message": "PDF compressed successfully.",

        "file": {

            "id": file.id,

            "original_name": file.original_name,

            "output_name": output_filename,

            "output_path": result["output"]

        },

        "compression": {

            "target_size_kb": result[
                "target_size_kb"
            ],

            "before_size": result[
                "before_size"
            ],

            "after_size": result[
                "after_size"
            ],

            "saved_bytes": result[
                "saved_bytes"
            ]

        }

    }


# ==========================================================
# DOWNLOAD COMPRESSED PDF
# ==========================================================

@router.get(
    "/download-compressed",
    summary="Download Compressed PDF"
)
def download_compressed_pdf(
    file_id: int = Query(
        ...,
        gt=0,
        description="ID file PDF"
    ),

    target_size_kb: int = Query(
        ...,
        gt=0,
        description="Target ukuran PDF dalam KB"
    ),

    db: Session = Depends(
        get_db
    ),

    current_user=Depends(
        get_current_active_user
    )
):

    # ------------------------------------------------------
    # SERVICE
    # ------------------------------------------------------

    service = CompressService(
        db
    )

    # ------------------------------------------------------
    # GET FILE
    # ------------------------------------------------------

    file = service.get_file(
        file_id
    )

    # ------------------------------------------------------
    # CHECK USER
    # ------------------------------------------------------

    if file.user_id != current_user.id:

        raise HTTPException(
            status_code=403,
            detail="You do not have permission to access this file."
        )

    # ------------------------------------------------------
    # ORIGINAL PATH
    # ------------------------------------------------------

    input_path = Path(
    file.storage_path
    )

    # ------------------------------------------------------
    # COMPRESSED DIRECTORY
    # ------------------------------------------------------

    compressed_directory = (
    input_path.parent /
    "compressed"
    )

    # ------------------------------------------------------
    # FIND COMPRESSED FILE
    # ------------------------------------------------------

    pattern = (
    f"{input_path.stem}_"
    f"compressed_"
    f"{target_size_kb}kb"
    f"_level_*.pdf"
    )

    compressed_files = sorted(
    compressed_directory.glob(
        pattern
    ),
    key=lambda path: path.stat().st_mtime,
    reverse=True
    )

    # ------------------------------------------------------
    # CHECK FILE
    # ------------------------------------------------------
    if not compressed_files:
        raise HTTPException(
        status_code=404,
        detail="Compressed PDF not found."
    )

    # ------------------------------------------------------
    # SELECT LATEST COMPRESSED FILE
    # ------------------------------------------------------

    output_path = compressed_files[0]

    output_filename = output_path.name

    # ------------------------------------------------------
    # DOWNLOAD
    # ------------------------------------------------------

    return FileResponse(
    path=str(output_path),
    filename=output_filename,
    media_type="application/pdf"
    )


# ==========================================================
# MERGE PDF
# ==========================================================

@router.post(
    "/merge",
    summary="Merge PDF files"
)
def merge_pdf(
    file_ids: list[int],
    db: Session = Depends(
        get_db
    ),
    current_user=Depends(
        get_current_active_user
    )
):

    # ------------------------------------------------------
    # VALIDATE INPUT
    # ------------------------------------------------------

    if len(file_ids) < 2:

        raise HTTPException(
            status_code=400,
            detail="Minimal 2 file PDF diperlukan."
        )

    if len(file_ids) > 20:

        raise HTTPException(
            status_code=400,
            detail="Maksimal 20 file PDF dapat digabung sekaligus."
        )

    # ------------------------------------------------------
    # GET FILES
    # ------------------------------------------------------

    files = []

    for file_id in file_ids:

        file = db.query(
            File
        ).filter(
            File.id == file_id
        ).first()

        if file is None:

            raise HTTPException(
                status_code=404,
                detail=f"File dengan ID {file_id} tidak ditemukan."
            )

        # --------------------------------------------------
        # CHECK OWNER
        # --------------------------------------------------

        if file.user_id != current_user.id:

            raise HTTPException(
                status_code=403,
                detail="You do not have permission to access this file."
            )

        files.append(
            file
        )

    # ------------------------------------------------------
    # OUTPUT DIRECTORY
    # ------------------------------------------------------

    input_path = Path(
        files[0].storage_path
    )

    output_directory = (
        input_path.parent /
        "merged"
    )

    output_directory.mkdir(
        parents=True,
        exist_ok=True
    )

    # ------------------------------------------------------
    # OUTPUT FILE
    # ------------------------------------------------------

    output_filename = (
        f"merged_{files[0].id}_"
        f"{len(files)}_files.pdf"
    )

    output_path = (
        output_directory /
        output_filename
    )

    # ------------------------------------------------------
    # MERGE
    # ------------------------------------------------------

    service = MergeService(
        db
    )

    try:

        result = service.execute(
            file_ids=file_ids,
            output_path=str(
                output_path
            )
        )

    except Exception as exc:

        raise HTTPException(
            status_code=400,
            detail=str(exc)
        )
# ------------------------------------------------------
    # SAVE MERGED FILE
    # ------------------------------------------------------

    try:

        merged_file = File(
            user_id=current_user.id,
            original_name=output_filename,
            stored_name=f"{uuid4().hex}.pdf",
            file_extension=".pdf",
            mime_type="application/pdf",
            file_size=Path(result).stat().st_size,
            storage_path=str(result),
            status="completed"
        )

        file_repository = FileRepository(db)

        merged_file = file_repository.create(
            merged_file
        )

    except Exception as exc:

        raise HTTPException(
            status_code=500,
            detail=f"Failed to save merged file: {str(exc)}"
        )
        # ------------------------------------------------------
    # RESPONSE
    # ------------------------------------------------------

    return {
        "success": True,
        "message": "PDF files merged successfully.",
        "files": {
            "count": len(files),
            "ids": file_ids
        },
        "output": {
    "id": merged_file.id,
    "name": output_filename,
    "path": result
}
    }



# ==========================================================
# ==========================================================
# PDF TO WORD
# ==========================================================

@router.post(
    "/to-word",
    summary="Convert PDF to Word"
)
def pdf_to_word(
    file_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_active_user)
):

    # ------------------------------------------------------
    # GET FILE
    # ------------------------------------------------------

    file = db.query(
        File
    ).filter(
        File.id == file_id
    ).first()

    if file is None:
        raise HTTPException(
            status_code=404,
            detail="File PDF tidak ditemukan."
        )

    # ------------------------------------------------------
    # CHECK OWNER
    # ------------------------------------------------------

    if file.user_id != current_user.id:
        raise HTTPException(
            status_code=403,
            detail="You do not have permission to access this file."
        )

    # ------------------------------------------------------
    # CHECK PDF
    # ------------------------------------------------------

    if file.mime_type != "application/pdf":
        raise HTTPException(
            status_code=400,
            detail="File yang dipilih bukan PDF."
        )

    # ------------------------------------------------------
    # OUTPUT
    # ------------------------------------------------------

    input_path = Path(
        file.storage_path
    )

    output_directory = (
        input_path.parent /
        "word"
    )

    output_path = (
        output_directory /
        f"{input_path.stem}.docx"
    )

    # ------------------------------------------------------
    # CONVERT
    # ------------------------------------------------------

    service = PdfToWordService(
        db
    )

    try:

        result = service.convert(
            pdf_path=str(input_path),
            output_path=str(output_path)
        )

    except Exception as exc:

        raise HTTPException(
            status_code=400,
            detail=str(exc)
        )

    # ------------------------------------------------------
    # SAVE WORD FILE
    # ------------------------------------------------------

    try:

        file_repository = FileRepository(
            db
        )

        word_path = Path(
            result
        )

        word_file = File(
            user_id=current_user.id,
            original_name=word_path.name,
            stored_name=word_path.name,
            file_extension=".docx",
            mime_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
            file_size=word_path.stat().st_size,
            storage_path=str(word_path),
            status="completed"
        )

        word_file = file_repository.create(
            word_file
        )

    except Exception as exc:

        raise HTTPException(
            status_code=500,
            detail=f"Gagal menyimpan hasil Word: {str(exc)}"
        )

    # ------------------------------------------------------
    # RESPONSE
    # ------------------------------------------------------

    return {
        "success": True,
        "message": "PDF berhasil dikonversi ke Word.",
        "source": {
            "id": file.id,
            "name": file.original_name
        },
        "output": {
            "id": word_file.id,
            "name": word_file.original_name,
            "path": word_file.storage_path,
            "size": word_file.file_size
        }
    }

# PDF TO JPG
# ==========================================================

@router.post(
    "/to-jpg",
    summary="Convert PDF to JPG"
)
def pdf_to_jpg(
    file_id: int,
    dpi: int = 150,
    pages: str | None = Query(None, description="Pilihan halaman misal: '2' atau '1-3' atau '1,3,5'"),
    db: Session = Depends(get_db),
    current_user=Depends(get_current_active_user)
):

    # ------------------------------------------------------
    # GET FILE
    # ------------------------------------------------------

    file = db.query(
        File
    ).filter(
        File.id == file_id
    ).first()

    if file is None:

        raise HTTPException(
            status_code=404,
            detail="File PDF tidak ditemukan."
        )

    # ------------------------------------------------------
    # CHECK OWNER
    # ------------------------------------------------------

    if file.user_id != current_user.id:

        raise HTTPException(
            status_code=403,
            detail="You do not have permission to access this file."
        )

    # ------------------------------------------------------
    # CHECK PDF
    # ------------------------------------------------------

    if file.mime_type != "application/pdf":

        raise HTTPException(
            status_code=400,
            detail="File yang dipilih bukan PDF."
        )

    # ------------------------------------------------------
    # OUTPUT DIRECTORY
    # ------------------------------------------------------

    input_path = Path(
        file.storage_path
    )

    output_directory = (
        input_path.parent /
        "jpg"
    )

    # ------------------------------------------------------
    # CONVERT
    # ------------------------------------------------------

    service = PdfToJpgService(
        db
    )

    try:

        output_files = service.convert(
            pages=pages,
            pdf_path=str(
                input_path
            ),
            output_directory=str(
                output_directory
            ),
            dpi=dpi
        )

    except Exception as exc:

        raise HTTPException(
            status_code=400,
            detail=str(exc)
        )

    # ------------------------------------------------------
    # SAVE JPG FILES
    # ------------------------------------------------------

    file_repository = FileRepository(
        db
    )

    jpg_files = []

    try:

        for output_file in output_files:

            output_path = Path(
                output_file
            )

            jpg_file = File(
                user_id=current_user.id,
                original_name=output_path.name,
                stored_name=output_path.name,
                file_extension=".jpg",
                mime_type="image/jpeg",
                file_size=output_path.stat().st_size,
                storage_path=str(output_path),
                status="completed"
            )

            jpg_file = file_repository.create(
                jpg_file
            )

            jpg_files.append(
                jpg_file
            )

    except Exception as exc:

        raise HTTPException(
            status_code=500,
            detail=f"Gagal menyimpan hasil JPG: {str(exc)}"
        )

    # ------------------------------------------------------
    # RESPONSE
    # ------------------------------------------------------

    return {
        "success": True,
        "message": "PDF berhasil dikonversi ke JPG.",
        "source": {
            "id": file.id,
            "name": file.original_name
        },
        "images": [
            {
                "id": jpg_file.id,
                "name": jpg_file.original_name,
                "path": jpg_file.storage_path,
                "size": jpg_file.file_size
            }
            for jpg_file in jpg_files
        ],
        "count": len(jpg_files)
    }


# ==========================================================
# UNLOCK PDF
# ==========================================================

@router.post(
    "/unlock",
    summary="Unlock PDF"
)
def unlock_pdf(
    file_id: int = Query(
        ...,
        gt=0,
        description="ID file PDF"
    ),

    password: str = Query(
        "",
        description="Password PDF"
    ),

    db: Session = Depends(
        get_db
    ),

    current_user=Depends(
        get_current_active_user
    )
):

    service = UnlockService(
        db
    )

    file = service.get_file(
        file_id
    )

    if file.user_id != current_user.id:

        raise HTTPException(
            status_code=403,
            detail="You do not have permission to access this file."
        )

    service.validate_pdf(
        file
    )

    input_path = Path(
        file.storage_path
    )

    output_directory = (
        input_path.parent /
        "unlocked"
    )

    output_directory.mkdir(
        parents=True,
        exist_ok=True
    )

    output_filename = (
        f"{input_path.stem}_unlocked.pdf"
    )

    output_path = (
        output_directory /
        output_filename
    )

    try:

        result = service.execute(
            file_id=file_id,
            output_path=str(
                output_path
            ),
            password=password
        )

    except Exception as exc:

        raise HTTPException(
            status_code=400,
            detail=str(exc)
        )

    if not Path(result).exists():

        raise HTTPException(
            status_code=500,
            detail="Unlocked PDF was not created."
        )

    return FileResponse(
        path=str(result),
        filename=output_filename,
        media_type="application/pdf"
    )


# ==========================================================
# SPLIT PDF
# ==========================================================

@router.post(
    "/split",
    summary="Split PDF",
    description="Split PDF into separate files, one file per page."
)
def split_pdf(
    file_id: int = Query(
        ...,
        gt=0,
        description="ID file PDF"
    ),
    db: Session = Depends(get_db),
    current_user=Depends(get_current_active_user)
):

    service = SplitService(db)

    file = service.get_file(file_id)

    if file.user_id != current_user.id:
        raise HTTPException(
            status_code=403,
            detail="You do not have permission to access this file."
        )

    input_path = Path(file.storage_path)

    output_directory = (
        input_path.parent / "split"
    )

    output_directory.mkdir(
        parents=True,
        exist_ok=True
    )

    result = service.execute(
        file_id=file_id,
        output_directory=str(output_directory)
    )

    return {
        "success": True,
        "message": "PDF split successfully.",
        "file": {
            "id": file.id,
            "original_name": file.original_name
        },
        "files": [
            {
                "name": Path(output).name,
                "path": output
            }
            for output in result
        ],
        "count": len(result)
    }


