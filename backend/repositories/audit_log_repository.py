# ==========================================================
# PDF MASTER AI
# Audit Log Repository
# ==========================================================

# ----------------------------------------------------------
# IMPORT
# ----------------------------------------------------------

from sqlalchemy.orm import Session

from models.audit_log import AuditLog

from repositories.base_repository import BaseRepository

# ----------------------------------------------------------
# AUDIT LOG REPOSITORY
# ----------------------------------------------------------

class AuditLogRepository(

    BaseRepository[AuditLog]

):

    """
    Audit Log Repository.
    """

    def __init__(

        self,

        db: Session

    ):

        super().__init__(

            db,

            AuditLog

        )

    # ------------------------------------------------------
    # GET USER LOGS
    # ------------------------------------------------------

    def get_by_user(

        self,

        user_id: int

    ) -> list[AuditLog]:

        return (

            self.db.query(AuditLog)

            .filter(

                AuditLog.user_id == user_id

            )

            .order_by(

                AuditLog.created_at.desc()

            )

            .all()

        )

    # ------------------------------------------------------
    # GET ACTION
    # ------------------------------------------------------

    def get_by_action(

        self,

        action: str

    ) -> list[AuditLog]:

        return (

            self.db.query(AuditLog)

            .filter(

                AuditLog.action == action

            )

            .order_by(

                AuditLog.created_at.desc()

            )

            .all()

        )

    # ------------------------------------------------------
    # GET USER ACTION
    # ------------------------------------------------------

    def get_user_action(

        self,

        user_id: int,

        action: str

    ) -> list[AuditLog]:

        return (

            self.db.query(AuditLog)

            .filter(

                AuditLog.user_id == user_id,

                AuditLog.action == action

            )

            .order_by(

                AuditLog.created_at.desc()

            )

            .all()

        )

    # ------------------------------------------------------
    # GET IP ADDRESS
    # ------------------------------------------------------

    def get_by_ip(

        self,

        ip_address: str

    ) -> list[AuditLog]:

        return (

            self.db.query(AuditLog)

            .filter(

                AuditLog.ip_address == ip_address

            )

            .order_by(

                AuditLog.created_at.desc()

            )

            .all()

        )

    # ------------------------------------------------------
    # DELETE USER LOGS
    # ------------------------------------------------------

    def delete_by_user(

        self,

        user_id: int

    ) -> int:

        deleted = (

            self.db.query(AuditLog)

            .filter(

                AuditLog.user_id == user_id

            )

            .delete()

        )

        self.db.commit()

        return deleted

    # ------------------------------------------------------
    # COUNT USER LOGS
    # ------------------------------------------------------

    def count_by_user(

        self,

        user_id: int

    ) -> int:

        return (

            self.db.query(AuditLog)

            .filter(

                AuditLog.user_id == user_id

            )

            .count()

        )

    # ------------------------------------------------------
    # COUNT ACTION
    # ------------------------------------------------------

    def count_by_action(

        self,

        action: str

    ) -> int:

        return (

            self.db.query(AuditLog)

            .filter(

                AuditLog.action == action

            )

            .count()

        )