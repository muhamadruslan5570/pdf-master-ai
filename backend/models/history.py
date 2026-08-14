# ==========================================================
# PDF MASTER AI
# History Model
# ==========================================================

# ----------------------------------------------------------
# IMPORT
# ----------------------------------------------------------

from sqlalchemy import (
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
# HISTORY MODEL
# ----------------------------------------------------------

class History(BaseModel):

    __tablename__ = "histories"

    # ------------------------------------------------------
    # USER
    # ------------------------------------------------------

    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id"),
        nullable=False
    )

    # ------------------------------------------------------
    # FILE
    # ------------------------------------------------------

    file_id: Mapped[int] = mapped_column(
        ForeignKey("files.id"),
        nullable=False
    )

    # ------------------------------------------------------
    # ACTIVITY
    # ------------------------------------------------------

    action: Mapped[str] = mapped_column(
        String(100),
        nullable=False
    )

    category: Mapped[str] = mapped_column(
        String(50),
        nullable=False
    )

    status: Mapped[str] = mapped_column(
        String(30),
        default="completed",
        nullable=False
    )

    # ------------------------------------------------------
    # RESULT
    # ------------------------------------------------------

    result_file: Mapped[str | None] = mapped_column(
        String(500),
        nullable=True
    )

    message: Mapped[str | None] = mapped_column(
        Text,
        nullable=True
    )

    # ------------------------------------------------------
    # RELATIONSHIP
    # ------------------------------------------------------

    user = relationship(
        "User",
        back_populates="histories"
    )

    file = relationship(
        "File",
        back_populates="histories"
    )