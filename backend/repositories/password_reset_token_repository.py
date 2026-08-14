# ==========================================================
# PDF MASTER AI
# Password Reset Token Repository
# ==========================================================

# ----------------------------------------------------------
# IMPORT
# ----------------------------------------------------------

from datetime import datetime

from sqlalchemy.orm import Session

from models.password_reset_token import PasswordResetToken

from repositories.base_repository import BaseRepository


# ----------------------------------------------------------
# PASSWORD RESET TOKEN REPOSITORY
# ----------------------------------------------------------

class PasswordResetTokenRepository(
    BaseRepository[PasswordResetToken]
):

    """
    Password Reset Token Repository.
    """

    def __init__(
        self,
        db: Session
    ):

        super().__init__(
            db,
            PasswordResetToken
        )


    # ------------------------------------------------------
    # GET BY TOKEN HASH
    # ------------------------------------------------------

    def get_by_token_hash(
        self,
        token_hash: str
    ) -> PasswordResetToken | None:

        return (
            self.db.query(
                PasswordResetToken
            )
            .filter(
                PasswordResetToken.token_hash
                == token_hash
            )
            .first()
        )


    # ------------------------------------------------------
    # GET VALID TOKEN
    # ------------------------------------------------------

    def get_valid_token(
        self,
        token_hash: str
    ) -> PasswordResetToken | None:

        now = datetime.utcnow()

        return (
            self.db.query(
                PasswordResetToken
            )
            .filter(
                PasswordResetToken.token_hash
                == token_hash,

                PasswordResetToken.used_at
                .is_(None),

                PasswordResetToken.expires_at
                > now
            )
            .first()
        )


    # ------------------------------------------------------
    # GET USER TOKENS
    # ------------------------------------------------------

    def get_user_tokens(
        self,
        user_id: int
    ) -> list[PasswordResetToken]:

        return (
            self.db.query(
                PasswordResetToken
            )
            .filter(
                PasswordResetToken.user_id
                == user_id
            )
            .all()
        )


    # ------------------------------------------------------
    # GET ACTIVE USER TOKEN
    # ------------------------------------------------------

    def get_active_user_token(
        self,
        user_id: int
    ) -> PasswordResetToken | None:

        now = datetime.utcnow()

        return (
            self.db.query(
                PasswordResetToken
            )
            .filter(
                PasswordResetToken.user_id
                == user_id,

                PasswordResetToken.used_at
                .is_(None),

                PasswordResetToken.expires_at
                > now
            )
            .first()
        )


    # ------------------------------------------------------
    # MARK AS USED
    # ------------------------------------------------------

    def mark_as_used(
        self,
        token: PasswordResetToken
    ) -> PasswordResetToken:

        token.used_at = datetime.utcnow()

        return self.update(
            token
        )


    # ------------------------------------------------------
    # DELETE USER TOKENS
    # ------------------------------------------------------

    def delete_user_tokens(
        self,
        user_id: int
    ) -> None:

        tokens = self.get_user_tokens(
            user_id
        )

        for token in tokens:

            self.db.delete(
                token
            )

        self.db.commit()