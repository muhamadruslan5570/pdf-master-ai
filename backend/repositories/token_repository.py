# ==========================================================
# PDF MASTER AI
# Token Repository
# ==========================================================

# ----------------------------------------------------------
# IMPORT
# ----------------------------------------------------------

from sqlalchemy.orm import Session

from models.token import Token

from repositories.base_repository import BaseRepository

# ----------------------------------------------------------
# TOKEN REPOSITORY
# ----------------------------------------------------------

class TokenRepository(

    BaseRepository[Token]

):

    """
    Token Repository.
    """

    def __init__(

        self,

        db: Session

    ):

        super().__init__(

            db,

            Token

        )

    # ------------------------------------------------------
    # GET TOKEN
    # ------------------------------------------------------

    def get_by_token(

        self,

        token: str

    ) -> Token | None:

        return (

            self.db.query(Token)

            .filter(

                Token.token == token

            )

            .first()

        )

    # ------------------------------------------------------
    # GET USER TOKEN
    # ------------------------------------------------------

    def get_user_tokens(

        self,

        user_id: int

    ) -> list[Token]:

        return (

            self.db.query(Token)

            .filter(

                Token.user_id == user_id

            )

            .all()

        )

    # ------------------------------------------------------
    # GET TOKEN TYPE
    # ------------------------------------------------------

    def get_by_type(

        self,

        user_id: int,

        token_type: str

    ) -> list[Token]:

        return (

            self.db.query(Token)

            .filter(

                Token.user_id == user_id,

                Token.token_type == token_type

            )

            .all()

        )

    # ------------------------------------------------------
    # TOKEN EXISTS
    # ------------------------------------------------------

    def token_exists(

        self,

        token: str

    ) -> bool:

        return (

            self.get_by_token(

                token

            )

            is not None

        )

    # ------------------------------------------------------
    # DELETE TOKEN
    # ------------------------------------------------------

    def delete_token(

        self,

        token: Token

    ) -> None:

        self.db.delete(

            token

        )

        self.db.commit()

    # ------------------------------------------------------
    # DELETE USER TOKENS
    # ------------------------------------------------------

    def delete_user_tokens(

        self,

        user_id: int

    ) -> int:

        deleted = (

            self.db.query(Token)

            .filter(

                Token.user_id == user_id

            )

            .delete()

        )

        self.db.commit()

        return deleted

    # ------------------------------------------------------
    # DELETE TOKEN TYPE
    # ------------------------------------------------------

    def delete_by_type(

        self,

        user_id: int,

        token_type: str

    ) -> int:

        deleted = (

            self.db.query(Token)

            .filter(

                Token.user_id == user_id,

                Token.token_type == token_type

            )

            .delete()

        )

        self.db.commit()

        return deleted

    # ------------------------------------------------------
    # REVOKE TOKEN
    # ------------------------------------------------------

    def revoke(

        self,

        token: Token

    ) -> Token:

        token.is_revoked = True

        self.db.commit()

        self.db.refresh(

            token

        )

        return token

    # ------------------------------------------------------
    # ACTIVE TOKENS
    # ------------------------------------------------------

    def get_active_tokens(

        self,

        user_id: int

    ) -> list[Token]:

        return (

            self.db.query(Token)

            .filter(

                Token.user_id == user_id,

                Token.is_revoked == False

            )

            .all()

        )