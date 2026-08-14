# ==========================================================
# PDF MASTER AI
# Database Session
# ==========================================================

# ----------------------------------------------------------
# IMPORT
# ----------------------------------------------------------

from sqlalchemy.orm import sessionmaker

from database.connection import engine

# ----------------------------------------------------------
# SESSION FACTORY
# ----------------------------------------------------------

SessionLocal = sessionmaker(

    autocommit=False,

    autoflush=False,

    bind=engine

)

# ----------------------------------------------------------
# DATABASE SESSION
# ----------------------------------------------------------

def get_db():

    db = SessionLocal()

    try:

        yield db

    finally:

        db.close()