# ==========================================================
# PDF MASTER AI
# Security Utilities
# ==========================================================

# ----------------------------------------------------------
# IMPORT
# ----------------------------------------------------------

import secrets
import string
import hashlib

# ----------------------------------------------------------
# RANDOM STRING
# ----------------------------------------------------------

def generate_random_string(length: int = 32) -> str:
    """
    Generate secure random string.
    """

    characters = (
        string.ascii_letters +
        string.digits
    )

    return "".join(
        secrets.choice(characters)
        for _ in range(length)
    )

# ----------------------------------------------------------
# API KEY
# ----------------------------------------------------------

def generate_api_key() -> str:
    """
    Generate API Key.
    """

    return "pmai_" + generate_random_string(48)

# ----------------------------------------------------------
# EMAIL VERIFICATION TOKEN
# ----------------------------------------------------------

def generate_verification_token() -> str:
    """
    Generate email verification token.
    """

    return generate_random_string(64)

# ----------------------------------------------------------
# RESET PASSWORD TOKEN
# ----------------------------------------------------------

def generate_reset_token() -> str:
    """
    Generate password reset token.
    """

    return generate_random_string(64)

# ----------------------------------------------------------
# FILE NAME
# ----------------------------------------------------------

def generate_file_name(extension: str) -> str:
    """
    Generate unique file name.
    """

    return (
        generate_random_string(32)
        + "."
        + extension.lower()
    )

# ----------------------------------------------------------
# SHA256 HASH
# ----------------------------------------------------------

def sha256(value: str) -> str:
    """
    SHA256 Hash.
    """

    return hashlib.sha256(
        value.encode("utf-8")
    ).hexdigest()

# ----------------------------------------------------------
# CHECK API KEY
# ----------------------------------------------------------

def is_valid_api_key(api_key: str) -> bool:
    """
    Check API Key format.
    """

    return api_key.startswith("pmai_") and len(api_key) >= 40

# ----------------------------------------------------------
# MASK EMAIL
# ----------------------------------------------------------

def mask_email(email: str) -> str:
    """
    Hide email.
    """

    name, domain = email.split("@")

    if len(name) <= 2:
        return "*" * len(name) + "@" + domain

    return (
        name[:2]
        + "*" * (len(name) - 2)
        + "@"
        + domain
    )

# ----------------------------------------------------------
# MASK API KEY
# ----------------------------------------------------------

def mask_api_key(api_key: str) -> str:
    """
    Hide API Key.
    """

    if len(api_key) < 12:
        return api_key

    return (
        api_key[:8]
        + "..."
        + api_key[-6:]
    )