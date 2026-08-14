# ==========================================================
# PDF MASTER AI
# Token Model
# ==========================================================

# ----------------------------------------------------------
# IMPORT
# ----------------------------------------------------------

from datetime import datetime

from sqlalchemy import (
    Boolean,
    DateTime,
    ForeignKey,
    String
)

from sqlalchemy.orm import (
    Mapped,
    mapped_column,
    relationship
)

from models.base_model import BaseModel

# ----------------------------------------------------------
# TOKEN MODEL
# ----------------------------------------------------------

class Token(BaseModel):

    __tablename__ = "tokens"

    # ------------------------------------------------------
    # USER
    # ------------------------------------------------------

    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id"),
        nullable=False
    )

    # ------------------------------------------------------
    # TOKEN
    # ------------------------------------------------------

    access_token: Mapped[str] = mapped_column(
        String(500),
        nullable=False,
        unique=True
    )

    refresh_token: Mapped[str] = mapped_column(
        String(500),
        nullable=False,
        unique=True
    )

    # ------------------------------------------------------
    # DEVICE
    # ------------------------------------------------------

    device_name: Mapped[str | None] = mapped_column(
        String(150),
        nullable=True
    )

    ip_address: Mapped[str | None] = mapped_column(
        String(100),
        nullable=True
    )

    user_agent: Mapped[str | None] = mapped_column(
        String(500),
        nullable=True
    )

    # ------------------------------------------------------
    # STATUS
    # ------------------------------------------------------

    is_revoked: Mapped[bool] = mapped_column(
        Boolean,
        default=False
    )

    expires_at: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=False
    )

    # ------------------------------------------------------
    # RELATIONSHIP
    # ------------------------------------------------------

    user = relationship(
        "User",
        back_populates="tokens"
    )