from core.security import get_password_hash
from fastapi import APIRouter, HTTPException
from models.models import insert_user, select_user

router =APIRouter()

@router.post("/sign")
async def register_user(name: str, email: str, password: str, role: str):
    """
    Registers a new user in the system.
    Args:
        name (str): The name of the user.
        email (str): The email address of the user.
        password (str): The password for the user account.
        role (str): The role assigned to the user.
    Raises:
        HTTPException: If the email is already registered.
    Returns:
        dict: A dictionary containing a success message and the new user's details.
    """
    if select_user(email) != None:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    else:
        hashed_password = get_password_hash(password)
        new_user=insert_user(name=name, email=email, password=hashed_password, role=role)
        return {"message":"User registered succesfully", "user":new_user}