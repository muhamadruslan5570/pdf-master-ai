# ==========================================================
# PDF MASTER AI
# File Exceptions
# ==========================================================

# ----------------------------------------------------------
# IMPORT
# ----------------------------------------------------------

from fastapi import (
    HTTPException,
    status
)

# ----------------------------------------------------------
# FILE NOT FOUND
# ----------------------------------------------------------

class FileNotFoundException(

    HTTPException

):

    def __init__(self):

        super().__init__(

            status_code=status.HTTP_404_NOT_FOUND,

            detail="File not found."

        )

# ----------------------------------------------------------
# FILE TOO LARGE
# ----------------------------------------------------------

class FileTooLargeException(

    HTTPException

):

    def __init__(self):

        super().__init__(

            status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,

            detail="File size exceeds the maximum allowed limit."

        )

# ----------------------------------------------------------
# INVALID FILE TYPE
# ----------------------------------------------------------

class InvalidFileTypeException(

    HTTPException

):

    def __init__(

        self,

        file_type: str = "File"

    ):

        super().__init__(

            status_code=status.HTTP_400_BAD_REQUEST,

            detail=f"{file_type} type is not supported."

        )

# ----------------------------------------------------------
# INVALID MIME TYPE
# ----------------------------------------------------------

class InvalidMimeTypeException(

    HTTPException

):

    def __init__(self):

        super().__init__(

            status_code=status.HTTP_400_BAD_REQUEST,

            detail="Invalid MIME type."

        )

# ----------------------------------------------------------
# FILE UPLOAD FAILED
# ----------------------------------------------------------

class FileUploadException(

    HTTPException

):

    def __init__(self):

        super().__init__(

            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,

            detail="Failed to upload file."

        )

# ----------------------------------------------------------
# FILE DELETE FAILED
# ----------------------------------------------------------

class FileDeleteException(

    HTTPException

):

    def __init__(self):

        super().__init__(

            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,

            detail="Failed to delete file."

        )

# ----------------------------------------------------------
# FILE PROCESS FAILED
# ----------------------------------------------------------

class FileProcessException(

    HTTPException

):

    def __init__(

        self,

        process: str = "File"

    ):

        super().__init__(

            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,

            detail=f"{process} process failed."

        )

# ----------------------------------------------------------
# STORAGE ERROR
# ----------------------------------------------------------

class StorageException(

    HTTPException

):

    def __init__(self):

        super().__init__(

            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,

            detail="Storage service unavailable."

        )