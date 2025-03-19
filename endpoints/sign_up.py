import sqlite3
from core.security import get_password_hash
from fastapi import APIRouter, HTTPException
from models.models import insert_user, select_user

router =APIRouter()

@router.post("/sign")
async def register_user(name: str, email: str, password: str, role: str):
    if select_user(email) != None:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    else:
        hashed_password = get_password_hash(password)
        new_user=insert_user(name=name, email=email, password=hashed_password, role=role)
        return {"message":"Y=User registered succesfully", "user":new_user}