# ==========================================================
# PDF MASTER AI
# Database Connection
# ==========================================================

# ----------------------------------------------------------
# IMPORT
# ----------------------------------------------------------

import os

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.engine import URL

# ----------------------------------------------------------
# LOAD ENVIRONMENT
# ----------------------------------------------------------

load_dotenv()

# ----------------------------------------------------------
# DATABASE CONFIGURATION
# ----------------------------------------------------------

DATABASE_HOST = os.getenv("DATABASE_HOST", "127.0.0.1")
DATABASE_PORT = int(os.getenv("DATABASE_PORT", "5432"))
DATABASE_NAME = os.getenv("DATABASE_NAME", "pdf_master_ai")
DATABASE_USER = os.getenv("DATABASE_USER", "postgres")
DATABASE_PASSWORD = os.getenv("DATABASE_PASSWORD", "")

# ----------------------------------------------------------
# SQLALCHEMY URL
# ----------------------------------------------------------

DATABASE_URL = URL.create(
    drivername="postgresql+psycopg2",
    username=DATABASE_USER,
    password=DATABASE_PASSWORD,
    host=DATABASE_HOST,
    port=DATABASE_PORT,
    database=DATABASE_NAME,
)

# ----------------------------------------------------------
# SQLALCHEMY ENGINE
# ----------------------------------------------------------

engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True,
    pool_recycle=300,
    echo=False,
)