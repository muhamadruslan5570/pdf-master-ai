# ==========================================================
# PDF MASTER AI
# Validation Exceptions
# ==========================================================

# ----------------------------------------------------------
# IMPORT
# ----------------------------------------------------------

from fastapi import (
    HTTPException,
    status
)

# ----------------------------------------------------------
# VALIDATION ERROR
# ----------------------------------------------------------

class ValidationException(

    HTTPException

):

    def __init__(

        self,

        message: str = "Validation failed."

    ):

        super().__init__(

            status_code=status.HTTP_400_BAD_REQUEST,

            detail=message

        )

# ----------------------------------------------------------
# INVALID EMAIL
# ----------------------------------------------------------

class InvalidEmailException(

    HTTPException

):

    def __init__(self):

        super().__init__(

            status_code=status.HTTP_400_BAD_REQUEST,

            detail="Invalid email address."

        )

# ----------------------------------------------------------
# INVALID USERNAME
# ----------------------------------------------------------

class InvalidUsernameException(

    HTTPException

):

    def __init__(self):

        super().__init__(

            status_code=status.HTTP_400_BAD_REQUEST,

            detail="Invalid username."

        )

# ----------------------------------------------------------
# WEAK PASSWORD
# ----------------------------------------------------------

class WeakPasswordException(

    HTTPException

):

    def __init__(self):

        super().__init__(

            status_code=status.HTTP_400_BAD_REQUEST,

            detail="Password is too weak."

        )

# ----------------------------------------------------------
# REQUIRED FIELD
# ----------------------------------------------------------

class RequiredFieldException(

    HTTPException

):

    def __init__(

        self,

        field: str

    ):

        super().__init__(

            status_code=status.HTTP_400_BAD_REQUEST,

            detail=f"{field} is required."

        )

# ----------------------------------------------------------
# INVALID VALUE
# ----------------------------------------------------------

class InvalidValueException(

    HTTPException

):

    def __init__(

        self,

        field: str

    ):

        super().__init__(

            status_code=status.HTTP_400_BAD_REQUEST,

            detail=f"Invalid value for '{field}'."

        )

# ----------------------------------------------------------
# VALUE OUT OF RANGE
# ----------------------------------------------------------

class ValueOutOfRangeException(

    HTTPException

):

    def __init__(

        self,

        field: str

    ):

        super().__init__(

            status_code=status.HTTP_400_BAD_REQUEST,

            detail=f"'{field}' is out of the allowed range."

        )

# ----------------------------------------------------------
# INVALID FORMAT
# ----------------------------------------------------------

class InvalidFormatException(

    HTTPException

):

    def __init__(

        self,

        field: str

    ):

        super().__init__(

            status_code=status.HTTP_400_BAD_REQUEST,

            detail=f"Invalid format for '{field}'."

        )

# ----------------------------------------------------------
# INVALID REQUEST
# ----------------------------------------------------------

class InvalidRequestException(

    HTTPException

):

    def __init__(self):

        super().__init__(

            status_code=status.HTTP_400_BAD_REQUEST,

            detail="Invalid request."

        )