# ==========================================================
# PDF MASTER AI
# Base Repository
# ==========================================================

# ----------------------------------------------------------
# IMPORT
# ----------------------------------------------------------

from typing import Generic
from typing import Type
from typing import TypeVar

from sqlalchemy.orm import Session

from models.base_model import BaseModel

# ----------------------------------------------------------
# TYPE
# ----------------------------------------------------------

ModelType = TypeVar(

    "ModelType",

    bound=BaseModel

)

# ----------------------------------------------------------
# BASE REPOSITORY
# ----------------------------------------------------------

class BaseRepository(

    Generic[ModelType]

):

    """
    Base Repository.
    """

    def __init__(

        self,

        db: Session,

        model: Type[ModelType]

    ):

        self.db = db

        self.model = model

    # ------------------------------------------------------
    # GET BY ID
    # ------------------------------------------------------

    def get_by_id(

        self,

        record_id: int

    ) -> ModelType | None:

        return (

            self.db.query(self.model)

            .filter(

                self.model.id == record_id

            )

            .first()

        )

    # ------------------------------------------------------
    # GET ALL
    # ------------------------------------------------------

    def get_all(

        self

    ) -> list[ModelType]:

        return (

            self.db.query(

                self.model

            )

            .all()

        )

    # ------------------------------------------------------
    # CREATE
    # ------------------------------------------------------

    def create(

        self,

        obj: ModelType

    ) -> ModelType:

        self.db.add(obj)

        self.db.commit()

        self.db.refresh(obj)

        return obj

    # ------------------------------------------------------
    # UPDATE
    # ------------------------------------------------------

    def update(

        self,

        obj: ModelType

    ) -> ModelType:

        self.db.commit()

        self.db.refresh(obj)

        return obj

    # ------------------------------------------------------
    # DELETE
    # ------------------------------------------------------

    def delete(

        self,

        obj: ModelType

    ) -> None:

        self.db.delete(obj)

        self.db.commit()

    # ------------------------------------------------------
    # EXISTS
    # ------------------------------------------------------

    def exists(

        self,

        record_id: int

    ) -> bool:

        return (

            self.get_by_id(

                record_id

            )

            is not None

        )

    # ------------------------------------------------------
    # COUNT
    # ------------------------------------------------------

    def count(

        self

    ) -> int:

        return (

            self.db.query(

                self.model

            )

            .count()

        )