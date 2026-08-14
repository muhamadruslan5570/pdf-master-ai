# ==========================================================
# PDF MASTER AI
# Audit Log Schemas
# ==========================================================

# ----------------------------------------------------------
# IMPORT
# ----------------------------------------------------------

from datetime import datetime
from enum import Enum

from pydantic import Field

from schemas.base import BaseSchema

# ----------------------------------------------------------
# AUDIT MODULE
# ----------------------------------------------------------

class AuditModule(str, Enum):

    AUTH = "auth"

    USER = "user"

    PROFILE = "profile"

    SUBSCRIPTION = "subscription"

    PAYMENT = "payment"

    PDF = "pdf"

    CONVERT = "convert"

    IMAGE = "image"

    OFFICE = "office"

    ARCHIVE = "archive"

    AI = "ai"

    API = "api"

    SYSTEM = "system"

# ----------------------------------------------------------
# AUDIT ACTION
# ----------------------------------------------------------

class AuditAction(str, Enum):

    LOGIN = "login"

    LOGOUT = "logout"

    REGISTER = "register"

    VERIFY_EMAIL = "verify_email"

    CHANGE_PASSWORD = "change_password"

    UPDATE_PROFILE = "update_profile"

    DELETE_ACCOUNT = "delete_account"

    CREATE = "create"

    UPDATE = "update"

    DELETE = "delete"

    UPLOAD = "upload"

    DOWNLOAD = "download"

    COMPRESS = "compress"

    CONVERT = "convert"

    PROCESS = "process"

# ----------------------------------------------------------
# AUDIT STATUS
# ----------------------------------------------------------

class AuditStatus(str, Enum):

    SUCCESS = "success"

    FAILED = "failed"

    WARNING = "warning"

# ----------------------------------------------------------
# AUDIT BASE
# ----------------------------------------------------------

class AuditLogBase(BaseSchema):

    module: AuditModule

    action: AuditAction

    description: str | None = Field(
        default=None,
        max_length=1000
    )

# ----------------------------------------------------------
# CREATE AUDIT LOG
# ----------------------------------------------------------

class AuditLogCreate(AuditLogBase):

    user_id: int

# ----------------------------------------------------------
# UPDATE AUDIT LOG
# ----------------------------------------------------------

class AuditLogUpdate(BaseSchema):

    description: str | None = None

    status: AuditStatus | None = None

# ----------------------------------------------------------
# AUDIT LOG DETAIL
# ----------------------------------------------------------

class AuditLogDetail(AuditLogBase):

    id: int

    user_id: int

    ip_address: str | None

    user_agent: str | None

    status: AuditStatus

    created_at: datetime

    updated_at: datetime

# ----------------------------------------------------------
# AUDIT LOG RESPONSE
# ----------------------------------------------------------

class AuditLogResponse(BaseSchema):

    success: bool = True

    message: str

    data: AuditLogDetail

# ----------------------------------------------------------
# AUDIT LOG LIST RESPONSE
# ----------------------------------------------------------

class AuditLogListResponse(BaseSchema):

    success: bool = True

    total: int

    audit_logs: list[AuditLogDetail]