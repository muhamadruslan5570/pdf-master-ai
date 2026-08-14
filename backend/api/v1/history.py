from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from dependencies.database import get_db
from dependencies.current_user import get_current_active_user
from models.history import History
from models.user import User

router = APIRouter()


@router.get(
    "/my-history",
    summary="Get Current User History"
)
def my_history(
    db: Session = Depends(get_db),
    current_user: User = Depends(
        get_current_active_user
    )
):
    histories = (
        db.query(History)
        .filter(
            History.user_id == current_user.id
        )
        .order_by(
            History.created_at.desc()
        )
        .all()
    )

    return {
        "success": True,
        "data": [
            {
                "id": item.id,
                "user_id": item.user_id,
                "file_id": item.file_id,
                "action": item.action,
                "category": item.category,
                "status": item.status,
                "result_file": item.result_file,
                "message": item.message,
                "created_at": item.created_at,
                "updated_at": item.updated_at
            }
            for item in histories
        ],
        "total": len(histories)
    }
