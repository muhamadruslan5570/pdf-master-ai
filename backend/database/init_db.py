# ==========================================================
# PDF MASTER AI
# Database Initialization
# ==========================================================

# ----------------------------------------------------------
# IMPORT
# ----------------------------------------------------------

from database.connection import engine
from database.base import Base


# ----------------------------------------------------------
# IMPORT ALL MODELS
# ----------------------------------------------------------

from models.user import User
from models.subscription import Subscription
from models.payment import Payment
from models.file import File
from models.history import History
from models.api_key import APIKey
from models.token import Token
from models.audit_log import AuditLog
from models.password_reset_token import PasswordResetToken


# ----------------------------------------------------------
# CREATE DATABASE TABLES
# ----------------------------------------------------------

def init_database():

    Base.metadata.create_all(
        bind=engine
    )

    print("========================================")
    print(" PDF MASTER AI DATABASE INITIALIZED")
    print("========================================")


# ----------------------------------------------------------
# MAIN
# ----------------------------------------------------------

if __name__ == "__main__":

    init_database()