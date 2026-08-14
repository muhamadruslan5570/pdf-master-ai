# ==========================================================
# PDF MASTER AI
# API Key Dependency
# ==========================================================

# ----------------------------------------------------------
# IMPORT
# ----------------------------------------------------------

from fastapi import (

    Header,

    HTTPException,

    status

)

from core.security import is_valid_api_key

# ----------------------------------------------------------
# VERIFY API KEY
# ----------------------------------------------------------

def verify_api_key(

    x_api_key: str = Header(

        ...,

        alias="X-API-Key"

    )

) -> str:

    """
    Verify API Key format.
    """

    if not is_valid_api_key(

        x_api_key

    ):

        raise HTTPException(

            status_code=status.HTTP_401_UNAUTHORIZED,

            detail="Invalid API Key"

        )

    return x_api_key