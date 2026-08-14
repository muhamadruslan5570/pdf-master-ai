# ==========================================================
# PDF MASTER AI
# Payment Model
# ==========================================================

# ----------------------------------------------------------
# IMPORT
# ----------------------------------------------------------

from datetime import datetime

from sqlalchemy import (
    DateTime,
    ForeignKey,
    Numeric,
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
# PAYMENT MODEL
# ----------------------------------------------------------

class Payment(BaseModel):

    __tablename__ = "payments"

    # ------------------------------------------------------
    # RELATION
    # ------------------------------------------------------

    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id"),
        nullable=False
    )

    subscription_id: Mapped[int] = mapped_column(
        ForeignKey("subscriptions.id"),
        nullable=False
    )

    # ------------------------------------------------------
    # PAYMENT INFORMATION
    # ------------------------------------------------------

    invoice_number: Mapped[str] = mapped_column(
        String(100),
        unique=True,
        nullable=False
    )

    payment_method: Mapped[str] = mapped_column(
        String(50),
        nullable=False
    )

    payment_gateway: Mapped[str] = mapped_column(
        String(50),
        nullable=False
    )

    amount: Mapped[float] = mapped_column(
        Numeric(10,2),
        nullable=False
    )

    currency: Mapped[str] = mapped_column(
        String(10),
        default="IDR",
        nullable=False
    )

    # ------------------------------------------------------
    # STATUS
    # ------------------------------------------------------

    status: Mapped[str] = mapped_column(
        String(30),
        default="pending",
        nullable=False
    )

    transaction_id: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True
    )

    payment_date: Mapped[datetime | None] = mapped_column(
        DateTime,
        nullable=True
    )

    notes: Mapped[str | None] = mapped_column(
        Text,
        nullable=True
    )

    # ------------------------------------------------------
    # RELATIONSHIP
    # ------------------------------------------------------

    user = relationship(
        "User",
        back_populates="payments"
    )

    subscription = relationship(
        "Subscription",
        back_populates="payments"
    )