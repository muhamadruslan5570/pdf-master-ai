# ==========================================================
# PDF MASTER AI
# Base Model
# ==========================================================

# ----------------------------------------------------------
# IMPORT
# ----------------------------------------------------------

from datetime import datetime

from sqlalchemy import (
    DateTime,
    Integer
)

from sqlalchemy.orm import (
    Mapped,
    mapped_column
)

from database.base import Base

# ----------------------------------------------------------
# BASE MODEL
# ----------------------------------------------------------

class BaseModel(Base):

    __abstract__ = True

    # ------------------------------------------------------
    # PRIMARY KEY
    # ------------------------------------------------------

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        index=True
    )

    # ------------------------------------------------------
    # CREATED AT
    # ------------------------------------------------------

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        nullable=False
    )

    # ------------------------------------------------------
    # UPDATED AT
    # ------------------------------------------------------

    updated_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
        nullable=False
    )