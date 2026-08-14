# ==========================================================
# PDF MASTER AI
# API Key Service
# ==========================================================

# ----------------------------------------------------------
# IMPORT
# ----------------------------------------------------------

import secrets

from sqlalchemy.orm import Session

from repositories.api_key_repository import ApiKeyRepository

from repositories.user_repository import UserRepository

from models.api_key import ApiKey

from core.logger import info

from exceptions.database import (

    RecordNotFoundException

)

# ----------------------------------------------------------
# API KEY SERVICE
# ----------------------------------------------------------

class ApiKeyService:

    """
    User API Key Service.
    """

    def __init__(

        self,

        db: Session

    ):

        self.api_repository = ApiKeyRepository(

            db

        )

        self.user_repository = UserRepository(

            db

        )

    # ------------------------------------------------------
    # GET USER
    # ------------------------------------------------------

    def get_user(

        self,

        user_id: int

    ):

        user = self.user_repository.get_by_id(

            user_id

        )

        if user is None:

            raise RecordNotFoundException(

                "User"

            )

        return user

    # ------------------------------------------------------
    # GENERATE KEY
    # ------------------------------------------------------

    def generate_key(

        self

    ) -> str:

        return secrets.token_urlsafe(

            48

        )

    # ------------------------------------------------------
    # CREATE
    # ------------------------------------------------------

    def create(

        self,

        user_id: int,

        name: str = "Default API Key"

    ) -> ApiKey:

        self.get_user(

            user_id

        )

        api_key = ApiKey(

            user_id=user_id,

            name=name,

            api_key=self.generate_key(),

            is_active=True

        )

        api_key = self.api_repository.create(

            api_key

        )

        info(

            f"API Key created: {user_id}"

        )

        return api_key

    # ------------------------------------------------------
    # GET USER KEYS
    # ------------------------------------------------------

    def get_keys(

        self,

        user_id: int

    ):

        self.get_user(

            user_id

        )

        return self.api_repository.get_user_keys(

            user_id

        )

    # ------------------------------------------------------
    # REGENERATE
    # ------------------------------------------------------

    def regenerate(

        self,

        key_id: int

    ) -> ApiKey:

        api_key = self.api_repository.get_by_id(

            key_id

        )

        if api_key is None:

            raise RecordNotFoundException(

                "API Key"

            )

        api_key.api_key = self.generate_key()

        api_key = self.api_repository.update(

            api_key

        )

        info(

            f"API Key regenerated: {key_id}"

        )

        return api_key

    # ------------------------------------------------------
    # ACTIVATE
    # ------------------------------------------------------

    def activate(

        self,

        key_id: int

    ) -> ApiKey:

        api_key = self.api_repository.get_by_id(

            key_id

        )

        if api_key is None:

            raise RecordNotFoundException(

                "API Key"

            )

        return self.api_repository.activate(

            api_key

        )

    # ------------------------------------------------------
    # DEACTIVATE
    # ------------------------------------------------------

    def deactivate(

        self,

        key_id: int

    ) -> ApiKey:

        api_key = self.api_repository.get_by_id(

            key_id

        )

        if api_key is None:

            raise RecordNotFoundException(

                "API Key"

            )

        return self.api_repository.deactivate(

            api_key

        )

    # ------------------------------------------------------
    # DELETE
    # ------------------------------------------------------

    def delete(

        self,

        key_id: int

    ) -> None:

        api_key = self.api_repository.get_by_id(

            key_id

        )

        if api_key is None:

            raise RecordNotFoundException(

                "API Key"

            )

        self.api_repository.delete(

            api_key

        )

        info(

            f"API Key deleted: {key_id}"

        )