# ==========================================================
# PDF MASTER AI
# Base Schema
# ==========================================================

# ----------------------------------------------------------
# IMPORT
# ----------------------------------------------------------

from pydantic import BaseModel, ConfigDict

# ----------------------------------------------------------
# BASE SCHEMA
# ----------------------------------------------------------

class BaseSchema(BaseModel):

    model_config = ConfigDict(

        from_attributes=True,

        populate_by_name=True,

        str_strip_whitespace=True

    )