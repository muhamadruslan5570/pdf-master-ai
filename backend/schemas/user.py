# ==========================================================
# PDF MASTER AI
# User Schemas
# ==========================================================

from datetime import datetime
from pydantic import EmailStr, Field
from schemas.base import BaseSchema

class UserBase(BaseSchema):
    full_name: str = Field(min_length=3, max_length=150)
    username: str = Field(min_length=3, max_length=100)
    email: EmailStr

class UserCreate(UserBase):
    password: str = Field(min_length=8, max_length=100)

class UserUpdate(BaseSchema):
    full_name: str | None = Field(default=None, min_length=3, max_length=150)
    username: str | None = Field(default=None, min_length=3, max_length=100)
    email: EmailStr | None = None
    profile_image: str | None = None
    language: str | None = Field(default="id", max_length=10)
    theme: str | None = Field(default="light", max_length=20)
    auto_save: bool | None = True
    confirm_delete: bool | None = True
    pdf_quality: str | None = "recommended"
    process_notification: bool | None = True
    account_notification: bool | None = True
    email_notification: bool | None = False

class UserProfile(UserBase):
    id: int
    role: str
    profile_image: str | None = None
    is_active: bool
    is_verified: bool
    is_admin: bool
    language: str = "id"
    theme: str = "light"
    auto_save: bool = True
    confirm_delete: bool = True
    pdf_quality: str = "recommended"
    process_notification: bool = True
    account_notification: bool = True
    email_notification: bool = False
    created_at: datetime
    updated_at: datetime

class UserResponse(BaseSchema):
    success: bool = True
    message: str
    data: UserProfile

class UserListResponse(BaseSchema):
    success: bool = True
    total: int
    users: list[UserProfile]
