from fastapi import APIRouter, HTTPException, Depends, Request
from models.models import modify_user
from core.security import get_current_user

router =APIRouter(prefix="/user", tags=["athlete"])


@router.put("/modify")
async def modification_user(request: Request, data=dict, current_user: dict = Depends(get_current_user)):
    """
    Asynchronously modifies user information.
    Args:
        request (Request): The HTTP request object containing the user data.
        data (dict): A dictionary containing the user data to be modified.
        current_user (dict, optional): The current authenticated user. Defaults to the result of Depends(get_current_user).
    Raises:
        HTTPException: If the user is not authenticated (status code 401).
    Returns:
        The result of the modify_user function, which updates the user information.
    """
    if not current_user:
        raise HTTPException(status_code=401, detail="Authentication required")
    
    data = await request.json()
    user_id = current_user.get("id")

    return modify_user(id=user_id, **data)