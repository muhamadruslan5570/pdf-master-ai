# ==========================================================
# PDF MASTER AI
# Payment Repository
# ==========================================================

# ----------------------------------------------------------
# IMPORT
# ----------------------------------------------------------

from sqlalchemy.orm import Session

from models.payment import Payment

from repositories.base_repository import BaseRepository

from utils.helpers import utc_now

# ----------------------------------------------------------
# PAYMENT REPOSITORY
# ----------------------------------------------------------

class PaymentRepository(

    BaseRepository[Payment]

):

    """
    Payment Repository.
    """

    def __init__(

        self,

        db: Session

    ):

        super().__init__(

            db,

            Payment

        )

    # ------------------------------------------------------
    # GET USER PAYMENTS
    # ------------------------------------------------------

    def get_by_user(

        self,

        user_id: int

    ) -> list[Payment]:

        return (

            self.db.query(Payment)

            .filter(

                Payment.user_id == user_id

            )

            .order_by(

                Payment.created_at.desc()

            )

            .all()

        )

    # ------------------------------------------------------
    # GET INVOICE
    # ------------------------------------------------------

    def get_by_invoice(

        self,

        invoice_number: str

    ) -> Payment | None:

        return (

            self.db.query(Payment)

            .filter(

                Payment.invoice_number == invoice_number

            )

            .first()

        )

    # ------------------------------------------------------
    # GET TRANSACTION
    # ------------------------------------------------------

    def get_by_transaction(

        self,

        transaction_id: str

    ) -> Payment | None:

        return (

            self.db.query(Payment)

            .filter(

                Payment.transaction_id == transaction_id

            )

            .first()

        )

    # ------------------------------------------------------
    # GET STATUS
    # ------------------------------------------------------

    def get_by_status(

        self,

        status: str

    ) -> list[Payment]:

        return (

            self.db.query(Payment)

            .filter(

                Payment.status == status

            )

            .all()

        )

    # ------------------------------------------------------
    # PENDING
    # ------------------------------------------------------

    def get_pending(

        self

    ) -> list[Payment]:

        return self.get_by_status(

            "pending"

        )

    # ------------------------------------------------------
    # SUCCESS
    # ------------------------------------------------------

    def get_success(

        self

    ) -> list[Payment]:

        return self.get_by_status(

            "success"

        )

    # ------------------------------------------------------
    # FAILED
    # ------------------------------------------------------

    def get_failed(

        self

    ) -> list[Payment]:

        return self.get_by_status(

            "failed"

        )

    # ------------------------------------------------------
    # UPDATE STATUS
    # ------------------------------------------------------

    def update_status(

        self,

        payment: Payment,

        status: str

    ) -> Payment:

        payment.status = status

        self.db.commit()

        self.db.refresh(

            payment

        )

        return payment

    # ------------------------------------------------------
    # MARK PAID
    # ------------------------------------------------------

    def mark_paid(

        self,

        payment: Payment,

        transaction_id: str

    ) -> Payment:

        payment.status = "success"

        payment.transaction_id = transaction_id

        payment.payment_date = utc_now()

        self.db.commit()

        self.db.refresh(

            payment

        )

        return payment

    # ------------------------------------------------------
    # CANCEL
    # ------------------------------------------------------

    def cancel(

        self,

        payment: Payment

    ) -> Payment:

        payment.status = "cancelled"

        self.db.commit()

        self.db.refresh(

            payment

        )

        return payment