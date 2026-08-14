# ==========================================================
# PDF MASTER AI
# File Model
# ==========================================================

# ----------------------------------------------------------
# IMPORT
# ----------------------------------------------------------

from sqlalchemy import (
    BigInteger,
    ForeignKey,
    String,
    Text
)

from sqlalchemy.orm import (
    Mapped,
    mapped_column,
    relationship
)

from models.base_model import BaseModel

# ----------------------------------------------------------
# FILE MODEL
# ----------------------------------------------------------

class File(BaseModel):

    __tablename__ = "files"

    # ------------------------------------------------------
    # USER
    # ------------------------------------------------------

    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id"),
        nullable=False
    )

    # ------------------------------------------------------
    # FILE INFORMATION
    # ------------------------------------------------------

    original_name: Mapped[str] = mapped_column(
        String(255),
        nullable=False
    )

    stored_name: Mapped[str] = mapped_column(
        String(255),
        unique=True,
        nullable=False
    )

    file_extension: Mapped[str] = mapped_column(
        String(20),
        nullable=False
    )

    mime_type: Mapped[str] = mapped_column(
        String(100),
        nullable=False
    )

    file_size: Mapped[int] = mapped_column(
        BigInteger,
        nullable=False
    )

    # ------------------------------------------------------
    # STORAGE
    # ------------------------------------------------------

    storage_path: Mapped[str] = mapped_column(
        String(500),
        nullable=False
    )

    public_url: Mapped[str | None] = mapped_column(
        String(500),
        nullable=True
    )

    # ------------------------------------------------------
    # STATUS
    # ------------------------------------------------------

    status: Mapped[str] = mapped_column(
        String(30),
        default="uploaded",
        nullable=False
    )

    # ------------------------------------------------------
    # DESCRIPTION
    # ------------------------------------------------------

    description: Mapped[str | None] = mapped_column(
        Text,
        nullable=True
    )

    # ------------------------------------------------------
    # RELATIONSHIP
    # ------------------------------------------------------

    user = relationship(
        "User",
        back_populates="files"
    )

    histories = relationship(
        "History",
        back_populates="file",
        cascade="all, delete-orphan"
    )