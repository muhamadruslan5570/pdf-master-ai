# ==========================================================
# PDF MASTER AI
# Authentication Dependency
# ==========================================================

# ----------------------------------------------------------
# IMPORT
# ----------------------------------------------------------

from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer


# ----------------------------------------------------------
# OAUTH2 SCHEME
# ----------------------------------------------------------

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="/api/v1/auth/token"
)


# ----------------------------------------------------------
# GET ACCESS TOKEN
# ----------------------------------------------------------

def get_token(
    token: str = Depends(oauth2_scheme)
) -> str:

    """
    Get JWT Access Token from Authorization Header.
    """

    return token