# ==========================================================
# PDF MASTER AI
# Role & Permission Management
# ==========================================================

# ----------------------------------------------------------
# IMPORT
# ----------------------------------------------------------

from enum import Enum

# ----------------------------------------------------------
# USER ROLES
# ----------------------------------------------------------

class UserRole(str, Enum):

    USER = "user"

    PREMIUM = "premium"

    ADMIN = "admin"

    SUPERADMIN = "superadmin"

# ----------------------------------------------------------
# PERMISSIONS
# ----------------------------------------------------------

ROLE_PERMISSIONS = {

    UserRole.USER: {

        "profile.read",
        "profile.update",

        "file.upload",
        "file.download",
        "file.delete",

        "history.read",

        "subscription.read"

    },

    UserRole.PREMIUM: {

        "profile.read",
        "profile.update",

        "file.upload",
        "file.download",
        "file.delete",

        "history.read",

        "subscription.read",

        "premium.features",

        "ai.chat",

        "ai.summary",

        "api.use"

    },

    UserRole.ADMIN: {

        "*"

    },

    UserRole.SUPERADMIN: {

        "*"

    }

}

# ----------------------------------------------------------
# CHECK ROLE
# ----------------------------------------------------------

def has_role(
    user_role: str,
    required_role: str
) -> bool:

    return user_role == required_role

# ----------------------------------------------------------
# CHECK PERMISSION
# ----------------------------------------------------------

def has_permission(
    user_role: str,
    permission: str
) -> bool:

    permissions = ROLE_PERMISSIONS.get(

        UserRole(user_role),

        set()

    )

    if "*" in permissions:

        return True

    return permission in permissions

# ----------------------------------------------------------
# ADMIN
# ----------------------------------------------------------

def is_admin(user_role: str) -> bool:

    return user_role in (

        UserRole.ADMIN,

        UserRole.SUPERADMIN

    )

# ----------------------------------------------------------
# SUPER ADMIN
# ----------------------------------------------------------

def is_superadmin(user_role: str) -> bool:

    return user_role == UserRole.SUPERADMIN

# ----------------------------------------------------------
# PREMIUM
# ----------------------------------------------------------

def is_premium(user_role: str) -> bool:

    return user_role in (

        UserRole.PREMIUM,

        UserRole.ADMIN,

        UserRole.SUPERADMIN

    )