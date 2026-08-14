# ==========================================================
# PDF MASTER AI
# Subscription Model
# ==========================================================

# ----------------------------------------------------------
# IMPORT
# ----------------------------------------------------------

from datetime import datetime

from sqlalchemy import (
    Boolean,
    DateTime,
    ForeignKey,
    Numeric,
    String
)

from sqlalchemy.orm import (
    Mapped,
    mapped_column,
    relationship
)

from models.base_model import BaseModel

# ----------------------------------------------------------
# SUBSCRIPTION MODEL
# ----------------------------------------------------------

class Subscription(BaseModel):

    __tablename__ = "subscriptions"

    # ------------------------------------------------------
    # USER
    # ------------------------------------------------------

    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id"),
        nullable=False,
        unique=True
    )

    # ------------------------------------------------------
    # PLAN
    # ------------------------------------------------------

    plan_name: Mapped[str] = mapped_column(
        String(50),
        default="Free",
        nullable=False
    )

    plan_price: Mapped[float] = mapped_column(
        Numeric(10,2),
        default=0.00,
        nullable=False
    )

    billing_cycle: Mapped[str] = mapped_column(
        String(20),
        default="monthly",
        nullable=False
    )

    # ------------------------------------------------------
    # STATUS
    # ------------------------------------------------------

    status: Mapped[str] = mapped_column(
        String(20),
        default="active",
        nullable=False
    )

    is_active: Mapped[bool] = mapped_column(
        Boolean,
        default=True
    )

    # ------------------------------------------------------
    # PERIOD
    # ------------------------------------------------------

    start_date: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        nullable=False
    )

    end_date: Mapped[datetime | None] = mapped_column(
        DateTime,
        nullable=True
    )

    # ------------------------------------------------------
    # RELATIONSHIP
    # ------------------------------------------------------

    user = relationship(
        "User",
        back_populates="subscription"
    )

    payments = relationship(
        "Payment",
        back_populates="subscription",
        cascade="all, delete-orphan"
    )