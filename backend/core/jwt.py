# ==========================================================
# PDF MASTER AI
# JWT Utilities
# ==========================================================

# ----------------------------------------------------------
# IMPORT
# ----------------------------------------------------------

from datetime import (
    datetime,
    timedelta,
    timezone
)

from jose import (
    JWTError,
    jwt
)

from core.config import (
    SECRET_KEY,
    ALGORITHM,
    ACCESS_TOKEN_EXPIRE_MINUTES,
    REFRESH_TOKEN_EXPIRE_DAYS
)

# ==========================================================
# CREATE ACCESS TOKEN
# ==========================================================

def create_access_token(
    data: dict
) -> str:

    to_encode = data.copy()

    expire = datetime.now(
        timezone.utc
    ) + timedelta(
        minutes=ACCESS_TOKEN_EXPIRE_MINUTES
    )

    to_encode.update({
        "exp": expire,
        "type": "access"
    })

    return jwt.encode(
        to_encode,
        SECRET_KEY,
        algorithm=ALGORITHM
    )


# ==========================================================
# CREATE REFRESH TOKEN
# ==========================================================

def create_refresh_token(
    data: dict
) -> str:

    to_encode = data.copy()

    expire = datetime.now(
        timezone.utc
    ) + timedelta(
        days=REFRESH_TOKEN_EXPIRE_DAYS
    )

    to_encode.update({
        "exp": expire,
        "type": "refresh"
    })

    return jwt.encode(
        to_encode,
        SECRET_KEY,
        algorithm=ALGORITHM
    )


# ==========================================================
# CREATE RESET PASSWORD TOKEN
# ==========================================================

def create_reset_password_token(
    data: dict
) -> str:

    to_encode = data.copy()

    expire = datetime.now(
        timezone.utc
    ) + timedelta(
        minutes=30
    )

    to_encode.update({
        "exp": expire,
        "type": "reset_password"
    })

    return jwt.encode(
        to_encode,
        SECRET_KEY,
        algorithm=ALGORITHM
    )


# ==========================================================
# CREATE VERIFY EMAIL TOKEN
# ==========================================================

def create_verify_email_token(
    data: dict
) -> str:

    to_encode = data.copy()

    expire = datetime.now(
        timezone.utc
    ) + timedelta(
        minutes=30
    )

    to_encode.update({
        "exp": expire,
        "type": "verify_email"
    })

    return jwt.encode(
        to_encode,
        SECRET_KEY,
        algorithm=ALGORITHM
    )


# ==========================================================
# VERIFY TOKEN
# ==========================================================

def verify_token(
    token: str
):

    try:

        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM]
        )

        return payload

    except JWTError:

        return None


# ==========================================================
# GET USER ID
# ==========================================================

def get_user_id(
    token: str
):

    payload = verify_token(
        token
    )

    if payload is None:

        return None

    return payload.get(
        "user_id"
    )


# ==========================================================
# TOKEN TYPE
# ==========================================================

def get_token_type(
    token: str
):

    payload = verify_token(
        token
    )

    if payload is None:

        return None

    return payload.get(
        "type"
    )


# ==========================================================
# END
# ==========================================================