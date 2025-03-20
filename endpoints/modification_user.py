from core.security import get_password_hash
from fastapi import APIRouter, HTTPException, Depends, Request
from models.models import modify_user
from core.security import get_current_user

router =APIRouter(prefix="/user", tags=["athlete"])


@router.put("/modify")
async def modification_user(request: Request, data=dict, current_user: dict = Depends(get_current_user)):
    if not current_user:
        raise HTTPException(status_code=401, detail="Authentication required")
    
    data = await request.json()
    user_id = current_user.get("id")

    return modify_user(id=user_id, **data)