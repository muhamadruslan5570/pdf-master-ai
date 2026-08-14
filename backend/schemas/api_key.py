# ==========================================================
# PDF MASTER AI
# API Key Schemas
# ==========================================================

# ----------------------------------------------------------
# IMPORT
# ----------------------------------------------------------

from datetime import datetime
from enum import Enum

from pydantic import Field

from schemas.base import BaseSchema

# ----------------------------------------------------------
# API PERMISSION
# ----------------------------------------------------------

class APIPermission(str, Enum):

    READ = "read"

    WRITE = "write"

    ADMIN = "admin"

# ----------------------------------------------------------
# API STATUS
# ----------------------------------------------------------

class APIKeyStatus(str, Enum):

    ACTIVE = "active"

    DISABLED = "disabled"

    EXPIRED = "expired"

    REVOKED = "revoked"

# ----------------------------------------------------------
# API KEY BASE
# ----------------------------------------------------------

class APIKeyBase(BaseSchema):

    name: str = Field(
        min_length=3,
        max_length=100
    )

    permission: APIPermission = APIPermission.READ

# ----------------------------------------------------------
# CREATE API KEY
# ----------------------------------------------------------

class APIKeyCreate(APIKeyBase):

    user_id: int

# ----------------------------------------------------------
# UPDATE API KEY
# ----------------------------------------------------------

class APIKeyUpdate(BaseSchema):

    name: str | None = None

    permission: APIPermission | None = None

    status: APIKeyStatus | None = None

# ----------------------------------------------------------
# API KEY DETAIL
# ----------------------------------------------------------

class APIKeyDetail(APIKeyBase):

    id: int

    user_id: int

    api_key: str

    status: APIKeyStatus

    daily_limit: int

    requests_today: int

    expires_at: datetime | None

    created_at: datetime

    updated_at: datetime

# ----------------------------------------------------------
# API KEY RESPONSE
# ----------------------------------------------------------

class APIKeyResponse(BaseSchema):

    success: bool = True

    message: str

    data: APIKeyDetail

# ----------------------------------------------------------
# API KEY LIST RESPONSE
# ----------------------------------------------------------

class APIKeyListResponse(BaseSchema):

    success: bool = True

    total: int

    api_keys: list[APIKeyDetail]