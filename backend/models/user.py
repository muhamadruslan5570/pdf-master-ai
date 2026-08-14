# ==========================================================
# PDF MASTER AI
# User Model
# ==========================================================

# ----------------------------------------------------------
# IMPORT
# ----------------------------------------------------------

from sqlalchemy import (
    Boolean,
    String
)

from sqlalchemy.orm import (
    Mapped,
    mapped_column,
    relationship
)

from models.base_model import BaseModel


# ----------------------------------------------------------
# USER MODEL
# ----------------------------------------------------------

class User(BaseModel):

    __tablename__ = "users"


    # ------------------------------------------------------
    # ACCOUNT
    # ------------------------------------------------------

    full_name: Mapped[str] = mapped_column(
        String(150),
        nullable=False
    )

    username: Mapped[str] = mapped_column(
        String(100),
        unique=True,
        nullable=False,
        index=True
    )

    email: Mapped[str] = mapped_column(
        String(255),
        unique=True,
        nullable=False,
        index=True
    )

    password_hash: Mapped[str] = mapped_column(
        String(255),
        nullable=False
    )


    # ------------------------------------------------------
    # PROFILE
    # ------------------------------------------------------

    profile_image: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True
    )


    # ------------------------------------------------------
    # ROLE
    # ------------------------------------------------------

    role: Mapped[str] = mapped_column(
        String(50),
        default="user",
        nullable=False
    )


    # ------------------------------------------------------
    # STATUS
    # ------------------------------------------------------

    is_active: Mapped[bool] = mapped_column(
        Boolean,
        default=True
    )

    is_verified: Mapped[bool] = mapped_column(
        Boolean,
        default=False
    )

    is_admin: Mapped[bool] = mapped_column(
        Boolean,
        default=False
    )


    # ------------------------------------------------------
    

    # ------------------------------------------------------
    # PREFERENCES
    # ------------------------------------------------------

    language: Mapped[str] = mapped_column(
        String(10),
        default="id",
        nullable=False
    )

    theme: Mapped[str] = mapped_column(
        String(20),
        default="light",
        nullable=False
    )

    auto_save: Mapped[bool] = mapped_column(
        Boolean,
        default=True
    )

    confirm_delete: Mapped[bool] = mapped_column(
        Boolean,
        default=True
    )

    pdf_quality: Mapped[str] = mapped_column(
        String(20),
        default="recommended"
    )

    process_notification: Mapped[bool] = mapped_column(
        Boolean,
        default=True
    )

    account_notification: Mapped[bool] = mapped_column(
        Boolean,
        default=True
    )

    email_notification: Mapped[bool] = mapped_column(
        Boolean,
        default=False
    )

# RELATIONSHIPS
    # ------------------------------------------------------

    subscription = relationship(
        "Subscription",
        back_populates="user",
        uselist=False,
        cascade="all, delete-orphan"
    )

    payments = relationship(
        "Payment",
        back_populates="user",
        cascade="all, delete-orphan"
    )

    files = relationship(
        "File",
        back_populates="user",
        cascade="all, delete-orphan"
    )

    histories = relationship(
        "History",
        back_populates="user",
        cascade="all, delete-orphan"
    )

    api_keys = relationship(
        "APIKey",
        back_populates="user",
        cascade="all, delete-orphan"
    )

    tokens = relationship(
        "Token",
        back_populates="user",
        cascade="all, delete-orphan"
    )

    # ------------------------------------------------------
    # PASSWORD RESET TOKENS
    # ------------------------------------------------------

    password_reset_tokens = relationship(
        "PasswordResetToken",
        back_populates="user",
        cascade="all, delete-orphan"
    )

    audit_logs = relationship(
        "AuditLog",
        back_populates="user",
        cascade="all, delete-orphan"
    )

