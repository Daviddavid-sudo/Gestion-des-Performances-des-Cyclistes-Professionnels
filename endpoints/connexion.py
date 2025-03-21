from fastapi import APIRouter, HTTPException, Depends
from fastapi.responses import JSONResponse
from core.security import verify_password, create_access_token, get_password_hash, get_current_user
from models.models import select_user

router= APIRouter(tags=['login'])

@router.post("/login")
async def login(email: str, password: str):
    """
    Allows user to connect to the API
    Args:
        email (str): email of the user
        password (str): password of the user
    Returns:
        Returns the user email and the access token.
    """ 
    user = select_user(email)
    if not user or not verify_password(password, get_password_hash(password)):
         raise HTTPException(status_code=400, detail="Invalid credentials")
    access_token = create_access_token(data={"sub": email})
    return  {"email": email, "access_token": access_token}

@router.get("/users/me")
async def get_user_me(current_user=Depends(get_current_user)):
    """
    Retrieve the details of the currently authenticated user.

    This endpoint allows a logged-in user to fetch their own profile information, 
    including their unique user ID, name, and email address.

    ### Returns:
        dict: A JSON object containing:
        - `id` (int): The unique identifier of the user.
        - `name` (str): The full name of the user.
        - `email` (str): The registered email address of the user.
    
    ### Raises:
        - **401 Unauthorized**: If the user is not authenticated or the token is invalid.

    """
    return {"id": current_user["id"], "name": current_user["name"], "email": current_user["email"]}
