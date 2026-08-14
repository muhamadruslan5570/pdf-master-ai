# ==========================================================
# PDF MASTER AI
# Password Reset Token Model
# ==========================================================

# ----------------------------------------------------------
# IMPORT
# ----------------------------------------------------------

from datetime import datetime

from sqlalchemy import (
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
# PASSWORD RESET TOKEN MODEL
# ----------------------------------------------------------

class PasswordResetToken(BaseModel):

    """
    Password reset token model.

    Stores a secure hash of the password reset token
    instead of the original token.
    """

    __tablename__ = "password_reset_tokens"


    # ------------------------------------------------------
    # USER
    # ------------------------------------------------------

    user_id: Mapped[int] = mapped_column(
        ForeignKey(
            "users.id",
            ondelete="CASCADE"
        ),
        nullable=False,
        index=True
    )


    # ------------------------------------------------------
    # TOKEN HASH
    # ------------------------------------------------------

    token_hash: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
        unique=True,
        index=True
    )


    # ------------------------------------------------------
    # EXPIRATION
    # ------------------------------------------------------

    expires_at: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=False,
        index=True
    )


    # ------------------------------------------------------
    # USED
    # ------------------------------------------------------

    used_at: Mapped[datetime | None] = mapped_column(
        DateTime,
        nullable=True
    )


    # ------------------------------------------------------
    # RELATIONSHIP
    # ------------------------------------------------------

    user = relationship(
        "User",
        back_populates="password_reset_tokens"
    )