# ==========================================================
# PDF MASTER AI
# Audit Log Model
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
# AUDIT LOG MODEL
# ----------------------------------------------------------

class AuditLog(BaseModel):

    __tablename__ = "audit_logs"

    # ------------------------------------------------------
    # USER
    # ------------------------------------------------------

    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id"),
        nullable=False
    )

    # ------------------------------------------------------
    # ACTION
    # ------------------------------------------------------

    action: Mapped[str] = mapped_column(
        String(100),
        nullable=False
    )

    module: Mapped[str] = mapped_column(
        String(100),
        nullable=False
    )

    description: Mapped[str | None] = mapped_column(
        Text,
        nullable=True
    )

    # ------------------------------------------------------
    # CLIENT INFORMATION
    # ------------------------------------------------------

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

    status: Mapped[str] = mapped_column(
        String(30),
        default="success",
        nullable=False
    )

    # ------------------------------------------------------
    # RELATIONSHIP
    # ------------------------------------------------------

    user = relationship(
        "User",
        back_populates="audit_logs"
    )