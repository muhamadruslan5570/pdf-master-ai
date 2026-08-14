# ==========================================================
# PDF MASTER AI
# Database Dependency
# ==========================================================

# ----------------------------------------------------------
# IMPORT
# ----------------------------------------------------------

from sqlalchemy.orm import Session

from database.session import SessionLocal

# ----------------------------------------------------------
# GET DATABASE
# ----------------------------------------------------------

def get_db():

    db: Session = SessionLocal()

    try:

        yield db

    finally:

        db.close()