from fastapi import APIRouter, HTTPException, Depends
from src.models.count_session_model import CountSessionCreate, CountSessionOut
from src.services.count_session_service import (
    create_count_session,
    list_count_sessions,
    get_count_session_by_id,
    update_count_session,
    delete_count_session
)
from src.auth import get_current_user
from src.models.user_model import UserOut

router = APIRouter(prefix="/countSessions", tags=["Count Sessions"])

@router.post("/", response_model=CountSessionOut)
def add_count_session(
    session: CountSessionCreate,
    current_user: UserOut = Depends(get_current_user)
):
    try:
        return create_count_session(session, user_id=current_user.id)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/", response_model=list[CountSessionOut])
def get_all_sessions():
    try:
        return list_count_sessions()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{id}", response_model=CountSessionOut)
def get_session(id: str):
    try:
        return get_count_session_by_id(id)
    except Exception as e:
        raise HTTPException(status_code=404, detail=f"Count session {id} not found: {str(e)}")


@router.put("/{id}", response_model=CountSessionOut)
def update_session(id: str, session: CountSessionCreate):
    try:
        return update_count_session(id, session)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.delete("/{id}", response_model=dict)
def delete_session(id: str):
    try:
        deleted = delete_count_session(id)
        return {"message": f"Sesión {id} eliminada correctamente", "deleted": deleted}
    except Exception as e:
        raise HTTPException(status_code=404, detail=f"Count session {id} not found: {str(e)}")
