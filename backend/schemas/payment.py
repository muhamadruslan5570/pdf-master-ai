# ==========================================================
# PDF MASTER AI
# Payment Schemas
# ==========================================================

# ----------------------------------------------------------
# IMPORT
# ----------------------------------------------------------

from datetime import datetime
from decimal import Decimal
from enum import Enum

from pydantic import Field

from schemas.base import BaseSchema

# ----------------------------------------------------------
# PAYMENT METHOD
# ----------------------------------------------------------

class PaymentMethod(str, Enum):

    CREDIT_CARD = "credit_card"

    DEBIT_CARD = "debit_card"

    BANK_TRANSFER = "bank_transfer"

    VIRTUAL_ACCOUNT = "virtual_account"

    E_WALLET = "e_wallet"

    QRIS = "qris"

    CASH = "cash"


# ----------------------------------------------------------
# PAYMENT GATEWAY
# ----------------------------------------------------------

class PaymentGateway(str, Enum):

    MANUAL = "manual"

    MIDTRANS = "midtrans"

    XENDIT = "xendit"

    STRIPE = "stripe"

    PAYPAL = "paypal"

    DANA = "dana"

    GOPAY = "gopay"

    OVO = "ovo"

    SHOPEEPAY = "shopeepay"

    LINKAJA = "linkaja"

    QRIS = "qris"

    BANK_TRANSFER = "bank_transfer"


# ----------------------------------------------------------
# PAYMENT STATUS
# ----------------------------------------------------------

class PaymentStatus(str, Enum):

    PENDING = "pending"

    PROCESSING = "processing"

    PAID = "paid"

    FAILED = "failed"

    EXPIRED = "expired"

    CANCELLED = "cancelled"

    REFUNDED = "refunded"


# ----------------------------------------------------------
# PAYMENT BASE
# ----------------------------------------------------------

class PaymentBase(BaseSchema):

    payment_method: PaymentMethod = PaymentMethod.E_WALLET

    payment_gateway: PaymentGateway = PaymentGateway.MANUAL

    amount: Decimal = Field(
        ge=0
    )

    currency: str = Field(
        default="IDR",
        max_length=10
    )


# ----------------------------------------------------------
# CREATE PAYMENT
# ----------------------------------------------------------

class PaymentCreate(PaymentBase):

    user_id: int

    subscription_id: int


# ----------------------------------------------------------
# UPDATE PAYMENT
# ----------------------------------------------------------

class PaymentUpdate(BaseSchema):

    payment_method: PaymentMethod | None = None

    payment_gateway: PaymentGateway | None = None

    status: PaymentStatus | None = None

    transaction_id: str | None = None

    payment_date: datetime | None = None

    notes: str | None = None


# ----------------------------------------------------------
# PAYMENT DETAIL
# ----------------------------------------------------------

class PaymentDetail(PaymentBase):

    id: int

    user_id: int

    subscription_id: int

    invoice_number: str

    transaction_id: str | None

    status: PaymentStatus

    payment_date: datetime | None

    notes: str | None

    created_at: datetime

    updated_at: datetime


# ----------------------------------------------------------
# PAYMENT RESPONSE
# ----------------------------------------------------------

class PaymentResponse(BaseSchema):

    success: bool = True

    message: str

    data: PaymentDetail


# ----------------------------------------------------------
# PAYMENT LIST RESPONSE
# ----------------------------------------------------------

class PaymentListResponse(BaseSchema):

    success: bool = True

    total: int

    payments: list[PaymentDetail]