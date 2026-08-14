# ==========================================================
# PDF MASTER AI
# Users API
# ==========================================================

from fastapi import (
    APIRouter,
    Depends,
    HTTPException
)

from pydantic import BaseModel, Field, EmailStr

from sqlalchemy.orm import Session

from dependencies.database import get_db

from models.user import User

from dependencies.current_user import (
    get_current_user
)


# ----------------------------------------------------------
# ROUTER
# ----------------------------------------------------------

router = APIRouter()

class UserProfileUpdate(BaseModel):
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



# ==========================================================
# CURRENT USER
# ==========================================================

@router.get(
    "/me",
    summary="Get Current User"
)
def get_me(
    current_user: User = Depends(
        get_current_user
    )
):

    # ------------------------------------------------------
    # SUBSCRIPTION
    # ------------------------------------------------------

    subscription = (
        current_user.subscription
    )

    subscription_data = None

    if subscription:

        subscription_data = {

            "id":
                subscription.id,

            "plan_name":
                subscription.plan_name,

            "plan_price":
                float(
                    subscription.plan_price
                ),

            "billing_cycle":
                subscription.billing_cycle,

            "status":
                subscription.status,

            "is_active":
                subscription.is_active,

            "start_date":
                subscription.start_date,

            "end_date":
                subscription.end_date

        }


    # ------------------------------------------------------
    # USER RESPONSE
    # ------------------------------------------------------

    return {

        "success": True,

        "user": {

            "id":
                current_user.id,

            "full_name":
                current_user.full_name,

            "username":
                current_user.username,

            "email":
                current_user.email,

            "profile_image":
                current_user.profile_image,

            "role":
                current_user.role,

            "is_active":
                current_user.is_active,

            "is_verified":
                current_user.is_verified,

            "is_admin":
                current_user.is_admin,

            "language":
                getattr(current_user, "language", "id"),

            "theme":
                getattr(current_user, "theme", "light"),

            "auto_save":
                getattr(current_user, "auto_save", True),

            "confirm_delete":
                getattr(current_user, "confirm_delete", True),

            "pdf_quality":
                getattr(current_user, "pdf_quality", "recommended"),

            "process_notification":
                getattr(current_user, "process_notification", True),

            "account_notification":
                getattr(current_user, "account_notification", True),

            "email_notification":
                getattr(current_user, "email_notification", False),

            "created_at":
                current_user.created_at,

            "updated_at":
                current_user.updated_at,

            "subscription":
                subscription_data

        }

    }


# ==========================================================
# UPDATE CURRENT USER PROFILE
# ==========================================================

@router.put(
    "/me",
    summary="Update Current User Profile"
)
def update_me(
    data: UserProfileUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(
        get_current_user
    )
):

    full_name = data.full_name.strip() if data.full_name else current_user.full_name
    username = data.username.strip() if data.username else current_user.username
    email = data.email.strip().lower() if data.email else current_user.email

    if not full_name:
        raise HTTPException(
            status_code=400,
            detail="Nama lengkap tidak boleh kosong."
        )

    if not username:
        raise HTTPException(
            status_code=400,
            detail="Username tidak boleh kosong."
        )

    if not email:
        raise HTTPException(
            status_code=400,
            detail="Email tidak boleh kosong."
        )

    username_exists = (
        db.query(User)
        .filter(
            User.username == username,
            User.id != current_user.id
        )
        .first()
    )

    if username_exists:
        raise HTTPException(
            status_code=400,
            detail="Username sudah digunakan."
        )

    email_exists = (
        db.query(User)
        .filter(
            User.email == email,
            User.id != current_user.id
        )
        .first()
    )

    if email_exists:
        raise HTTPException(
            status_code=400,
            detail="Email sudah digunakan."
        )

    current_user.full_name = full_name
    current_user.username = username
    current_user.email = email

    # Simpan preferensi pengguna jika dikirim
    if getattr(data, 'language', None) is not None:
        current_user.language = data.language.strip()
    if getattr(data, 'theme', None) is not None:
        current_user.theme = data.theme.strip()
    if getattr(data, 'auto_save', None) is not None:
        current_user.auto_save = data.auto_save
    if getattr(data, 'confirm_delete', None) is not None:
        current_user.confirm_delete = data.confirm_delete
    if getattr(data, 'pdf_quality', None) is not None:
        current_user.pdf_quality = data.pdf_quality.strip()
    if getattr(data, 'process_notification', None) is not None:
        current_user.process_notification = data.process_notification
    if getattr(data, 'account_notification', None) is not None:
        current_user.account_notification = data.account_notification
    if getattr(data, 'email_notification', None) is not None:
        current_user.email_notification = data.email_notification

    db.commit()
    db.refresh(current_user)

    return {
        "success": True,
        "message": "Profile berhasil diperbarui.",
        "user": {
            "id": current_user.id,
            "full_name": current_user.full_name,
            "username": current_user.username,
            "email": current_user.email,
            "profile_image": current_user.profile_image,
            "role": current_user.role,
            "is_active": current_user.is_active,
            "is_verified": current_user.is_verified,
            "is_admin": current_user.is_admin,
            "language": getattr(current_user, "language", "id"),
            "theme": getattr(current_user, "theme", "light"),
            "auto_save": getattr(current_user, "auto_save", True),
            "confirm_delete": getattr(current_user, "confirm_delete", True),
            "pdf_quality": getattr(current_user, "pdf_quality", "recommended"),
            "process_notification": getattr(current_user, "process_notification", True),
            "account_notification": getattr(current_user, "account_notification", True),
            "email_notification": getattr(current_user, "email_notification", False)
        }
    }


# ----------------------------------------------------------
# UPLOAD / UPDATE AVATAR
# ----------------------------------------------------------
from pathlib import Path
from uuid import uuid4
from fastapi import File, UploadFile

AVATAR_DIR = Path("storage/avatars")
AVATAR_DIR.mkdir(parents=True, exist_ok=True)

@router.post("/avatar", summary="Upload User Avatar")
async def upload_avatar(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    allowed_types = {"image/jpeg", "image/png", "image/webp"}
    if file.content_type not in allowed_types:
        raise HTTPException(
            status_code=400,
            detail="Format foto profil harus JPG, PNG, atau WEBP."
        )

    extension = Path(file.filename or "avatar.jpg").suffix.lower()
    if extension not in {".jpg", ".jpeg", ".png", ".webp"}:
        extension = ".jpg"

    filename = f"user_{current_user.id}_{uuid4().hex[:8]}{extension}"
    file_path = AVATAR_DIR / filename

    try:
        contents = await file.read()
        with open(file_path, "wb") as f:
            f.write(contents)

        avatar_url = f"/storage/avatars/{filename}"

        if hasattr(current_user, "avatar"):
            current_user.avatar = avatar_url
        if hasattr(current_user, "profile_image"):
            current_user.profile_image = avatar_url

        db.add(current_user)
        db.commit()
        db.refresh(current_user)

        return {
            "success": True,
            "message": "Foto profil berhasil diperbarui.",
            "avatar_url": avatar_url,
            "avatar": avatar_url
        }
    except Exception as error:
        db.rollback()
        if file_path.exists():
            file_path.unlink()
        raise HTTPException(
            status_code=500,
            detail=f"Gagal menyimpan avatar: {str(error)}"
        )
