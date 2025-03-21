from fastapi import APIRouter, HTTPException, Depends
from fastapi.responses import JSONResponse
from core.security import verify_password, create_access_token, get_password_hash, get_current_user
from models.models import select_user

router= APIRouter(tags=['login'])

@router.post("/login")
async def login(email: str, password: str):
    user = select_user(email)
    if not user or not verify_password(password, get_password_hash(password)):
         raise HTTPException(status_code=400, detail="Invalid credentials")
    access_token = create_access_token(data={"sub": email})
    return  {"email": email, "access_token": access_token}

@router.get("/users/me")
async def get_user_me(current_user=Depends(get_current_user)):
    return {"id": current_user["id"], "name": current_user["name"], "email": current_user["email"]}
