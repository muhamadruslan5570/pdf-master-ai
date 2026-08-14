# ==========================================================
# PDF MASTER AI
# Payment Exceptions
# ==========================================================

# ----------------------------------------------------------
# IMPORT
# ----------------------------------------------------------

from fastapi import (
    HTTPException,
    status
)

# ----------------------------------------------------------
# PAYMENT FAILED
# ----------------------------------------------------------

class PaymentFailedException(

    HTTPException

):

    def __init__(self):

        super().__init__(

            status_code=status.HTTP_400_BAD_REQUEST,

            detail="Payment failed."

        )

# ----------------------------------------------------------
# PAYMENT NOT FOUND
# ----------------------------------------------------------

class PaymentNotFoundException(

    HTTPException

):

    def __init__(self):

        super().__init__(

            status_code=status.HTTP_404_NOT_FOUND,

            detail="Payment not found."

        )

# ----------------------------------------------------------
# PAYMENT EXPIRED
# ----------------------------------------------------------

class PaymentExpiredException(

    HTTPException

):

    def __init__(self):

        super().__init__(

            status_code=status.HTTP_400_BAD_REQUEST,

            detail="Payment has expired."

        )

# ----------------------------------------------------------
# PAYMENT CANCELLED
# ----------------------------------------------------------

class PaymentCancelledException(

    HTTPException

):

    def __init__(self):

        super().__init__(

            status_code=status.HTTP_400_BAD_REQUEST,

            detail="Payment has been cancelled."

        )

# ----------------------------------------------------------
# PAYMENT ALREADY COMPLETED
# ----------------------------------------------------------

class PaymentAlreadyCompletedException(

    HTTPException

):

    def __init__(self):

        super().__init__(

            status_code=status.HTTP_409_CONFLICT,

            detail="Payment has already been completed."

        )

# ----------------------------------------------------------
# INVALID PAYMENT METHOD
# ----------------------------------------------------------

class InvalidPaymentMethodException(

    HTTPException

):

    def __init__(self):

        super().__init__(

            status_code=status.HTTP_400_BAD_REQUEST,

            detail="Invalid payment method."

        )

# ----------------------------------------------------------
# INVALID PAYMENT GATEWAY
# ----------------------------------------------------------

class InvalidPaymentGatewayException(

    HTTPException

):

    def __init__(self):

        super().__init__(

            status_code=status.HTTP_400_BAD_REQUEST,

            detail="Invalid payment gateway."

        )

# ----------------------------------------------------------
# PAYMENT GATEWAY ERROR
# ----------------------------------------------------------

class PaymentGatewayException(

    HTTPException

):

    def __init__(

        self,

        gateway: str = "Payment Gateway"

    ):

        super().__init__(

            status_code=status.HTTP_502_BAD_GATEWAY,

            detail=f"{gateway} service is unavailable."

        )

# ----------------------------------------------------------
# REFUND FAILED
# ----------------------------------------------------------

class RefundFailedException(

    HTTPException

):

    def __init__(self):

        super().__init__(

            status_code=status.HTTP_400_BAD_REQUEST,

            detail="Refund failed."

        )

# ----------------------------------------------------------
# SUBSCRIPTION REQUIRED
# ----------------------------------------------------------

class SubscriptionRequiredException(

    HTTPException

):

    def __init__(self):

        super().__init__(

            status_code=status.HTTP_403_FORBIDDEN,

            detail="Active subscription required."

        )
