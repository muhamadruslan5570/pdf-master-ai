# ==========================================================
# PDF MASTER AI
# Permission Dependencies
# ==========================================================

# ----------------------------------------------------------
# IMPORT
# ----------------------------------------------------------

from fastapi import (
    Depends,
    HTTPException,
    status
)

from models.user import User

from core.permissions import (

    is_admin,

    is_superadmin,

    is_premium,

    has_permission

)

from dependencies.current_user import (

    get_current_user

)

# ----------------------------------------------------------
# CURRENT ADMIN
# ----------------------------------------------------------

def get_current_admin(

    current_user: User = Depends(get_current_user)

) -> User:

    """
    Allow only Admin or Super Admin.
    """

    if not is_admin(current_user.role):

        raise HTTPException(

            status_code=status.HTTP_403_FORBIDDEN,

            detail="Administrator access required."

        )

    return current_user


# ----------------------------------------------------------
# CURRENT SUPER ADMIN
# ----------------------------------------------------------

def get_current_superadmin(

    current_user: User = Depends(get_current_user)

) -> User:

    """
    Allow only Super Admin.
    """

    if not is_superadmin(current_user.role):

        raise HTTPException(

            status_code=status.HTTP_403_FORBIDDEN,

            detail="Super Administrator access required."

        )

    return current_user


# ----------------------------------------------------------
# CURRENT PREMIUM USER
# ----------------------------------------------------------

def get_current_premium(

    current_user: User = Depends(get_current_user)

) -> User:

    """
    Allow Premium, Admin, or Super Admin.
    """

    if not is_premium(current_user.role):

        raise HTTPException(

            status_code=status.HTTP_403_FORBIDDEN,

            detail="Premium membership required."

        )

    return current_user


# ----------------------------------------------------------
# REQUIRE PERMISSION
# ----------------------------------------------------------

def require_permission(permission: str):

    """
    Permission dependency factory.
    """

    def permission_checker(

        current_user: User = Depends(get_current_user)

    ) -> User:

        if not has_permission(

            current_user.role,

            permission

        ):

            raise HTTPException(

                status_code=status.HTTP_403_FORBIDDEN,

                detail="Permission denied."

            )

        return current_user

    return permission_checker