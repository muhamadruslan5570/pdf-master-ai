# ==========================================================
# PDF MASTER AI
# Subscription Repository
# ==========================================================

# ----------------------------------------------------------
# IMPORT
# ----------------------------------------------------------

from sqlalchemy.orm import Session

from models.subscription import Subscription

from repositories.base_repository import BaseRepository

from utils.helpers import utc_now

# ----------------------------------------------------------
# SUBSCRIPTION REPOSITORY
# ----------------------------------------------------------

class SubscriptionRepository(

    BaseRepository[Subscription]

):

    """
    Subscription Repository.
    """

    def __init__(

        self,

        db: Session

    ):

        super().__init__(

            db,

            Subscription

        )

    # ------------------------------------------------------
    # GET USER SUBSCRIPTION
    # ------------------------------------------------------

    def get_by_user(

        self,

        user_id: int

    ) -> Subscription | None:

        return (

            self.db.query(Subscription)

            .filter(

                Subscription.user_id == user_id

            )

            .first()

        )

    # ------------------------------------------------------
    # ACTIVE SUBSCRIPTION
    # ------------------------------------------------------

    def get_active(

        self,

        user_id: int

    ) -> Subscription | None:

        return (

            self.db.query(Subscription)

            .filter(

                Subscription.user_id == user_id,

                Subscription.is_active == True

            )

            .first()

        )

    # ------------------------------------------------------
    # PLAN
    # ------------------------------------------------------

    def get_by_plan(

        self,

        plan: str

    ) -> list[Subscription]:

        return (

            self.db.query(Subscription)

            .filter(

                Subscription.plan == plan

            )

            .all()

        )

    # ------------------------------------------------------
    # ACTIVE
    # ------------------------------------------------------

    def activate(

        self,

        subscription: Subscription

    ) -> Subscription:

        subscription.is_active = True

        self.db.commit()

        self.db.refresh(subscription)

        return subscription

    # ------------------------------------------------------
    # DEACTIVATE
    # ------------------------------------------------------

    def deactivate(

        self,

        subscription: Subscription

    ) -> Subscription:

        subscription.is_active = False

        self.db.commit()

        self.db.refresh(subscription)

        return subscription

    # ------------------------------------------------------
    # EXTEND
    # ------------------------------------------------------

    def extend(

        self,

        subscription: Subscription,

        expires_at

    ) -> Subscription:

        subscription.expires_at = expires_at

        self.db.commit()

        self.db.refresh(subscription)

        return subscription

    # ------------------------------------------------------
    # EXPIRED
    # ------------------------------------------------------

    def get_expired(

        self

    ) -> list[Subscription]:

        return (

            self.db.query(Subscription)

            .filter(

                Subscription.expires_at < utc_now()

            )

            .all()

        )

    # ------------------------------------------------------
    # IS ACTIVE
    # ------------------------------------------------------

    def is_active(

        self,

        user_id: int

    ) -> bool:

        subscription = self.get_active(

            user_id

        )

        return subscription is not None