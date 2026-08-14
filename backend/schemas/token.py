# ==========================================================
# PDF MASTER AI
# Token Schemas
# ==========================================================

# ----------------------------------------------------------
# IMPORT
# ----------------------------------------------------------

from datetime import datetime
from enum import Enum

from schemas.base import BaseSchema

# ----------------------------------------------------------
# TOKEN TYPE
# ----------------------------------------------------------

class TokenType(str, Enum):

    BEARER = "Bearer"

# ----------------------------------------------------------
# TOKEN STATUS
# ----------------------------------------------------------

class TokenStatus(str, Enum):

    ACTIVE = "active"

    REVOKED = "revoked"

    EXPIRED = "expired"

# ----------------------------------------------------------
# TOKEN BASE
# ----------------------------------------------------------

class TokenBase(BaseSchema):

    access_token: str

    refresh_token: str

# ----------------------------------------------------------
# CREATE TOKEN
# ----------------------------------------------------------

class TokenCreate(TokenBase):

    user_id: int

# ----------------------------------------------------------
# UPDATE TOKEN
# ----------------------------------------------------------

class TokenUpdate(BaseSchema):

    is_revoked: bool | None = None

# ----------------------------------------------------------
# TOKEN DETAIL
# ----------------------------------------------------------

class TokenDetail(TokenBase):

    id: int

    user_id: int

    token_type: TokenType = TokenType.BEARER

    status: TokenStatus = TokenStatus.ACTIVE

    device_name: str | None

    ip_address: str | None

    user_agent: str | None

    expires_at: datetime

    created_at: datetime

    updated_at: datetime

# ----------------------------------------------------------
# TOKEN RESPONSE
# ----------------------------------------------------------

class TokenResponse(BaseSchema):

    success: bool = True

    message: str

    data: TokenDetail

# ----------------------------------------------------------
# TOKEN LIST RESPONSE
# ----------------------------------------------------------

class TokenListResponse(BaseSchema):

    success: bool = True

    total: int

    tokens: list[TokenDetail]