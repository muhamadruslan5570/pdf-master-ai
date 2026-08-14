# ==========================================================
# PDF MASTER AI
# User API
# ==========================================================

# ----------------------------------------------------------
# IMPORT
# ----------------------------------------------------------

from fastapi import APIRouter
from fastapi import Depends
from fastapi import Query
from fastapi import status

from sqlalchemy.orm import Session

from api.deps import get_db
from api.deps import CurrentUser

from services.user.user_service import UserService

from schemas.user import (

    UserCreate,

    UserUpdate,

    UserResponse,

    UserListResponse

)

# ----------------------------------------------------------
# ROUTER
# ----------------------------------------------------------

router = APIRouter()

# ----------------------------------------------------------
# GET USERS
# ----------------------------------------------------------

@router.get(

    "/",

    response_model=UserListResponse,

    summary="Get Users"

)
def get_users(

    page: int = Query(

        default=1,

        ge=1

    ),

    size: int = Query(

        default=20,

        ge=1,

        le=100

    ),

    db: Session = Depends(

        get_db

    ),

    current_user = CurrentUser

):

    service = UserService(

        db

    )

    return service.get_all(

        page=page,

        size=size

    )

# ----------------------------------------------------------
# GET USER
# ----------------------------------------------------------

@router.get(

    "/{user_id}",

    response_model=UserResponse,

    summary="Get User"

)
def get_user(

    user_id: int,

    db: Session = Depends(

        get_db

    ),

    current_user = CurrentUser

):

    service = UserService(

        db

    )

    return service.get_by_id(

        user_id

    )

# ----------------------------------------------------------
# CREATE USER
# ----------------------------------------------------------

@router.post(

    "/",

    response_model=UserResponse,

    status_code=status.HTTP_201_CREATED,

    summary="Create User"

)
def create_user(

    request: UserCreate,

    db: Session = Depends(

        get_db

    ),

    current_user = CurrentUser

):

    service = UserService(

        db

    )

    return service.create(

        request

    )

# ----------------------------------------------------------
# UPDATE USER
# ----------------------------------------------------------

@router.put(

    "/{user_id}",

    response_model=UserResponse,

    summary="Update User"

)
def update_user(

    user_id: int,

    request: UserUpdate,

    db: Session = Depends(

        get_db

    ),

    current_user = CurrentUser

):

    service = UserService(

        db

    )

    return service.update(

        user_id,

        request

    )

# ----------------------------------------------------------
# DELETE USER
# ----------------------------------------------------------

@router.delete(

    "/{user_id}",

    summary="Delete User"

)
def delete_user(

    user_id: int,

    db: Session = Depends(

        get_db

    ),

    current_user = CurrentUser

):

    service = UserService(

        db

    )

    service.delete(

        user_id

    )

    return {

        "success": True,

        "message": "User deleted successfully."

    }

# ----------------------------------------------------------
# PROFILE
# ----------------------------------------------------------

@router.get(

    "/me/profile",

    response_model=UserResponse,

    summary="My Profile"

)
def profile(

    current_user = CurrentUser

):

    return current_user