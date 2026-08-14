# ==========================================================
# PDF MASTER AI
# Password Utilities
# ==========================================================

# ----------------------------------------------------------
# IMPORT
# ----------------------------------------------------------

from passlib.context import CryptContext

# ----------------------------------------------------------
# PASSWORD CONTEXT
# ----------------------------------------------------------

pwd_context = CryptContext(

    schemes=["bcrypt"],

    deprecated="auto"

)

# ----------------------------------------------------------
# HASH PASSWORD
# ----------------------------------------------------------

def hash_password(password: str) -> str:
    """
    Hash plain password.
    """

    return pwd_context.hash(password)

# ----------------------------------------------------------
# VERIFY PASSWORD
# ----------------------------------------------------------

def verify_password(
    plain_password: str,
    hashed_password: str
) -> bool:
    """
    Verify password.
    """

    return pwd_context.verify(
        plain_password,
        hashed_password
    )

# ----------------------------------------------------------
# PASSWORD STRENGTH
# ----------------------------------------------------------

def is_strong_password(
    password: str
) -> bool:
    """
    Validate password strength.
    """

    if len(password) < 8:
        return False

    has_upper = any(c.isupper() for c in password)

    has_lower = any(c.islower() for c in password)

    has_digit = any(c.isdigit() for c in password)

    has_symbol = any(
        not c.isalnum()
        for c in password
    )

    return all([
        has_upper,
        has_lower,
        has_digit,
        has_symbol
    ])