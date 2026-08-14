# ==========================================================
# PDF MASTER AI
# Database Exceptions
# ==========================================================

# ----------------------------------------------------------
# IMPORT
# ----------------------------------------------------------

from fastapi import (
    HTTPException,
    status
)

# ----------------------------------------------------------
# DATABASE CONNECTION
# ----------------------------------------------------------

class DatabaseConnectionException(

    HTTPException

):

    def __init__(self):

        super().__init__(

            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,

            detail="Unable to connect to database."

        )

# ----------------------------------------------------------
# DATABASE ERROR
# ----------------------------------------------------------

class DatabaseException(

    HTTPException

):

    def __init__(

        self,

        message: str = "Database error."

    ):

        super().__init__(

            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,

            detail=message

        )

# ----------------------------------------------------------
# RECORD NOT FOUND
# ----------------------------------------------------------

class RecordNotFoundException(

    HTTPException

):

    def __init__(

        self,

        resource: str = "Record"

    ):

        super().__init__(

            status_code=status.HTTP_404_NOT_FOUND,

            detail=f"{resource} not found."

        )

# ----------------------------------------------------------
# DUPLICATE RECORD
# ----------------------------------------------------------

class DuplicateRecordException(

    HTTPException

):

    def __init__(

        self,

        resource: str = "Record"

    ):

        super().__init__(

            status_code=status.HTTP_409_CONFLICT,

            detail=f"{resource} already exists."

        )

# ----------------------------------------------------------
# DATABASE TRANSACTION
# ----------------------------------------------------------

class DatabaseTransactionException(

    HTTPException

):

    def __init__(self):

        super().__init__(

            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,

            detail="Database transaction failed."

        )

# ----------------------------------------------------------
# DATABASE TIMEOUT
# ----------------------------------------------------------

class DatabaseTimeoutException(

    HTTPException

):

    def __init__(self):

        super().__init__(

            status_code=status.HTTP_504_GATEWAY_TIMEOUT,

            detail="Database request timed out."

        )

# ----------------------------------------------------------
# FOREIGN KEY
# ----------------------------------------------------------

class ForeignKeyConstraintException(

    HTTPException

):

    def __init__(self):

        super().__init__(

            status_code=status.HTTP_409_CONFLICT,

            detail="Operation violates database constraints."

        )