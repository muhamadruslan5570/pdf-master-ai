# ==========================================================
# PDF MASTER AI
# API Key Model
# ==========================================================

# ----------------------------------------------------------
# IMPORT
# ----------------------------------------------------------

from datetime import datetime

from sqlalchemy import (
    Boolean,
    DateTime,
    ForeignKey,
    Integer,
    String
)

from sqlalchemy.orm import (
    Mapped,
    mapped_column,
    relationship
)

from models.base_model import BaseModel

# ----------------------------------------------------------
# API KEY MODEL
# ----------------------------------------------------------

class APIKey(BaseModel):

    __tablename__ = "api_keys"

    # ------------------------------------------------------
    # USER
    # ------------------------------------------------------

    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id"),
        nullable=False
    )

    # ------------------------------------------------------
    # API KEY
    # ------------------------------------------------------

    name: Mapped[str] = mapped_column(
        String(100),
        nullable=False
    )

    api_key: Mapped[str] = mapped_column(
        String(255),
        unique=True,
        nullable=False
    )

    # ------------------------------------------------------
    # PERMISSION
    # ------------------------------------------------------

    permission: Mapped[str] = mapped_column(
        String(100),
        default="read"
    )

    # ------------------------------------------------------
    # LIMIT
    # ------------------------------------------------------

    daily_limit: Mapped[int] = mapped_column(
        Integer,
        default=1000
    )

    requests_today: Mapped[int] = mapped_column(
        Integer,
        default=0
    )

    # ------------------------------------------------------
    # STATUS
    # ------------------------------------------------------

    is_active: Mapped[bool] = mapped_column(
        Boolean,
        default=True
    )

    expires_at: Mapped[datetime | None] = mapped_column(
        DateTime,
        nullable=True
    )

    # ------------------------------------------------------
    # RELATIONSHIP
    # ------------------------------------------------------

    user = relationship(
        "User",
        back_populates="api_keys"
    )