from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse
from core.security import verify_password, create_access_token, get_password_hash
from models.models import select_user

router= APIRouter(tags=['login'])

@router.post("/login")
async def login(email: str, password: str):
    """
    Permet à un utilisateur de se connecter""" 
    user = select_user(email)
    if not user or not verify_password(password, get_password_hash(password)):
         raise HTTPException(status_code=400, detail="Invalid credentials")
    access_token = create_access_token(data={"sub": email})
    return  {"email": email, "access_token": access_token}

    