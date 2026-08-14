# ==========================================================
# PDF MASTER AI
# Storage API
# ==========================================================

# ----------------------------------------------------------
# IMPORT
# ----------------------------------------------------------

from typing import List

from fastapi import APIRouter
from fastapi import Depends
from fastapi import File
from fastapi import UploadFile
from fastapi import Query
from fastapi import status

from fastapi.responses import FileResponse

from sqlalchemy.orm import Session

from dependencies.database import get_db

from dependencies.current_user import (
    get_current_active_user
)

from models.user import User

from services.storage.upload_service import UploadService
from services.storage.download_service import DownloadService
from services.storage.delete_service import DeleteService
from services.storage.file_manager_service import FileManagerService
from repositories.file_repository import FileRepository


# ----------------------------------------------------------
# ROUTER
# ----------------------------------------------------------

router = APIRouter()


# ==========================================================
# SINGLE UPLOAD
# ==========================================================

@router.post(
    "/upload",
    status_code=status.HTTP_201_CREATED,
    summary="Upload File"
)
async def upload(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(
        get_current_active_user
    )
):

    service = UploadService(
        db
    )

    uploaded_file = service.upload(
        upload_file=file,
        upload_directory="storage/uploads",
        user_id=current_user.id
    )

    return {
        "success": True,
        "message": "File uploaded successfully.",
        "file": {
            "id": uploaded_file.id,
            "original_name": uploaded_file.original_name,
            "stored_name": uploaded_file.stored_name,
            "file_extension": uploaded_file.file_extension,
            "mime_type": uploaded_file.mime_type,
            "file_size": uploaded_file.file_size,
            "storage_path": uploaded_file.storage_path,
            "status": uploaded_file.status
        }
    }

# ==========================================================
# MULTIPLE UPLOAD
# ==========================================================

@router.post(
    "/upload/multiple",
    summary="Upload Multiple Files"
)
async def upload_multiple(
    files: List[UploadFile] = File(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(
        get_current_active_user
    )
):

    service = UploadService(
        db
    )

    uploaded_files = service.upload_multiple(
        files=files,
        upload_directory="storage/uploads",
        user_id=current_user.id
    )

    return [
        {
            "id": uploaded_file.id,
            "original_name": uploaded_file.original_name,
            "stored_name": uploaded_file.stored_name,
            "file_extension": uploaded_file.file_extension,
            "mime_type": uploaded_file.mime_type,
            "file_size": uploaded_file.file_size,
            "storage_path": uploaded_file.storage_path,
            "status": uploaded_file.status
        }
        for uploaded_file in uploaded_files
    ]


# ==========================================================
# DOWNLOAD
# ==========================================================

@router.get(
    "/download/{file_id}",
    response_class=FileResponse,
    summary="Download File"
)
def download(
    file_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(
        get_current_active_user
    )
):

    service = DownloadService(
        db
    )

    return service.download(
        file_id
    )


# ==========================================================
# DELETE
# ==========================================================

# DELETE ALL CURRENT USER FILES
# ==========================================================

@router.delete(
    "/all",
    summary="Delete All Current User Files"
)
def delete_all(
    db: Session = Depends(get_db),
    current_user: User = Depends(
        get_current_active_user
    )
):

    service = DeleteService(
        db
    )

    deleted = service.hard_delete_all(
        current_user.id
    )

    return {
        "success": True,
        "message": "All files deleted successfully.",
        "deleted_count": deleted
    }


@router.delete(
    "/{file_id}",
    summary="Delete File"
)
def delete(
    file_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(
        get_current_active_user
    )
):

    service = DeleteService(
        db
    )

    service.hard_delete(
        file_id
    )

    return {
        "success": True,
        "message": "File deleted successfully."
    }



# ==========================================================
# MY FILES - DATABASE
# ==========================================================

@router.get(
    "/my-files",
    summary="Get Current User Files"
)
def my_files(
    db: Session = Depends(get_db),
    current_user: User = Depends(
        get_current_active_user
    )
):

    repository = FileRepository(
        db
    )

    files = repository.get_by_user(
        current_user.id
    )

    return {
        "success": True,
        "files": [

            {
                "id":
                    file.id,

                "original_name":
                    file.original_name,

                "stored_name":
                    file.stored_name,

                "file_extension":
                    file.file_extension,

                "mime_type":
                    file.mime_type,

                "file_size":
                    file.file_size,

                "storage_path":
                    file.storage_path,

                "public_url":
                    file.public_url,

                "status":
                    file.status,

                "description":
                    file.description,

                "created_at":
                    file.created_at,

                "updated_at":
                    file.updated_at

            }

            for file in files

        ]
    }

# ==========================================================
# STORAGE INFO
# ==========================================================

@router.get(
    "/info",
    summary="Storage Information"
)
def info(
    db: Session = Depends(get_db),
    current_user: User = Depends(
        get_current_active_user
    )
):

    manager = FileManagerService(
        db
    )

    return manager.storage_info(
        "storage/uploads"
    )


# ==========================================================
# LIST FILES
# ==========================================================

@router.get(
    "/files",
    summary="List Files"
)
def files(
    recursive: bool = Query(False),
    db: Session = Depends(get_db),
    current_user: User = Depends(
        get_current_active_user
    )
):

    manager = FileManagerService(
        db
    )

    return manager.list_files(
        "storage/uploads",
        recursive
    )


# ==========================================================
# SEARCH FILES
# ==========================================================

@router.get(
    "/search",
    summary="Search Files"
)
def search(
    keyword: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(
        get_current_active_user
    )
):

    manager = FileManagerService(
        db
    )

    return manager.search(
        "storage/uploads",
        keyword
    )