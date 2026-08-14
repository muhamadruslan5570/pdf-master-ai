# ==========================================================
# PDF MASTER AI
# Subscription Schemas
# ==========================================================

# ----------------------------------------------------------
# IMPORT
# ----------------------------------------------------------

from datetime import datetime

from decimal import Decimal

from pydantic import Field

from schemas.base import BaseSchema

# ----------------------------------------------------------
# SUBSCRIPTION BASE
# ----------------------------------------------------------

class SubscriptionBase(BaseSchema):

    plan_name: str = Field(
        min_length=3,
        max_length=50
    )

    billing_cycle: str = Field(
        default="monthly",
        pattern="^(monthly|yearly)$"
    )

# ----------------------------------------------------------
# CREATE SUBSCRIPTION
# ----------------------------------------------------------

class SubscriptionCreate(SubscriptionBase):

    user_id: int

    plan_price: Decimal = Field(
        default=0.00,
        ge=0
    )

# ----------------------------------------------------------
# UPDATE SUBSCRIPTION
# ----------------------------------------------------------

class SubscriptionUpdate(BaseSchema):

    plan_name: str | None = None

    billing_cycle: str | None = None

    plan_price: Decimal | None = None

    status: str | None = None

    is_active: bool | None = None

    end_date: datetime | None = None

# ----------------------------------------------------------
# SUBSCRIPTION DETAIL
# ----------------------------------------------------------

class SubscriptionDetail(SubscriptionBase):

    id: int

    user_id: int

    plan_price: Decimal

    status: str

    is_active: bool

    start_date: datetime

    end_date: datetime | None

    created_at: datetime

    updated_at: datetime

# ----------------------------------------------------------
# SUBSCRIPTION RESPONSE
# ----------------------------------------------------------

class SubscriptionResponse(BaseSchema):

    success: bool = True

    message: str

    data: SubscriptionDetail

# ----------------------------------------------------------
# SUBSCRIPTION LIST RESPONSE
# ----------------------------------------------------------

class SubscriptionListResponse(BaseSchema):

    success: bool = True

    total: int

    subscriptions: list[SubscriptionDetail]