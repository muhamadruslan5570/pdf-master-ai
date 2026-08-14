# ==========================================================
# PDF MASTER AI
# History API
# ==========================================================

# ----------------------------------------------------------
# IMPORT
# ----------------------------------------------------------

from fastapi import APIRouter
from fastapi import Depends
from fastapi import Query

from sqlalchemy.orm import Session

from api.deps import (
    get_db,
    CurrentUser
)

from services.history.history_service import HistoryService

# ----------------------------------------------------------
# ROUTER
# ----------------------------------------------------------

router = APIRouter()

# ==========================================================
# GET HISTORY
# ==========================================================

@router.get(

    "/",

    summary="Get History"

)
def get_history(

    page: int = Query(

        default=1,

        ge=1

    ),

    size: int = Query(

        default=20,

        ge=1,

        le=100

    ),

    db: Session = Depends(get_db),

    current_user = CurrentUser

):

    service = HistoryService(db)

    return service.get_all(

        user_id=current_user.id,

        page=page,

        size=size

    )

# ==========================================================
# GET HISTORY DETAIL
# ==========================================================

@router.get(

    "/{history_id}",

    summary="History Detail"

)
def get_history_detail(

    history_id: int,

    db: Session = Depends(get_db),

    current_user = CurrentUser

):

    service = HistoryService(db)

    return service.get_by_id(

        history_id

    )

# ==========================================================
# DELETE HISTORY
# ==========================================================

@router.delete(

    "/{history_id}",

    summary="Delete History"

)
def delete_history(

    history_id: int,

    db: Session = Depends(get_db),

    current_user = CurrentUser

):

    service = HistoryService(db)

    service.delete(

        history_id

    )

    return {

        "success": True,

        "message": "History deleted successfully."

    }

# ==========================================================
# CLEAR HISTORY
# ==========================================================

@router.delete(

    "/",

    summary="Clear History"

)
def clear_history(

    db: Session = Depends(get_db),

    current_user = CurrentUser

):

    service = HistoryService(db)

    service.clear(

        current_user.id

    )

    return {

        "success": True,

        "message": "History cleared successfully."

    }