from pathlib import Path
from uuid import uuid4

from fastapi import APIRouter, Depends, File, UploadFile, HTTPException
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session

from dependencies.database import get_db
from dependencies.current_user import get_current_active_user
from models.user import User

from services.image.enhance.service import ImageEnhanceService


router = APIRouter()


UPLOAD_DIR = Path("storage/image-enhance")
UPLOAD_DIR.mkdir(
    parents=True,
    exist_ok=True
)


@router.post(
    "/enhance",
    summary="Enhance Photo",
    description="Percantik dan tingkatkan kualitas foto."
)
async def enhance_photo(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(
        get_current_active_user
    )
):

    allowed_types = {
        "image/jpeg",
        "image/png",
        "image/webp"
    }

    if file.content_type not in allowed_types:
        raise HTTPException(
            status_code=400,
            detail="Format foto harus JPG, PNG, atau WEBP."
        )

    extension = (
        Path(file.filename or "image.jpg")
        .suffix
        .lower()
    )

    if extension not in {
        ".jpg",
        ".jpeg",
        ".png",
        ".webp"
    }:
        extension = ".jpg"

    unique_id = uuid4().hex

    input_path = (
        UPLOAD_DIR /
        f"{unique_id}_original{extension}"
    )

    output_path = (
        UPLOAD_DIR /
        f"{unique_id}_enhanced.jpg"
    )

    try:

        with open(
            input_path,
            "wb"
        ) as buffer:

            while True:

                chunk = await file.read(
                    1024 * 1024
                )

                if not chunk:
                    break

                buffer.write(chunk)

        service = ImageEnhanceService()

        result = service.enhance(
            input_path=str(input_path),
            output_path=str(output_path),
            scale=2,
            sharpness=1.5,
            contrast=1.1,
            color=1.05
        )

        return {
            "success": True,
            "message": "Foto berhasil dipercantik.",
            "original_name": file.filename,
            "output_name": output_path.name,
            "download_url": (
                f"/api/v1/image/download/"
                f"{output_path.name}"
            )
        }

    except Exception as error:

        if input_path.exists():
            input_path.unlink()

        if output_path.exists():
            output_path.unlink()

        raise HTTPException(
            status_code=500,
            detail=str(error)
        )


@router.get(
    "/download/{filename}",
    summary="Download Enhanced Photo"
)
def download_enhanced_photo(
    filename: str,
    current_user: User = Depends(
        get_current_active_user
    )
):

    file_path = (
        UPLOAD_DIR /
        Path(filename).name
    )

    if not file_path.exists():
        raise HTTPException(
            status_code=404,
            detail="Hasil foto tidak ditemukan."
        )

    return FileResponse(
        path=str(file_path),
        filename=file_path.name,
        media_type="image/jpeg"
    )
