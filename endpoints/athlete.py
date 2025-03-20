from core.security import get_password_hash
from fastapi import APIRouter, HTTPException, Depends
from models.models import insert_athlete, select_athlete
from core.security import get_current_user

router =APIRouter(prefix="/athlete", tags=["athlete"])

@router.post("/create")
async def register_user(athlete_id: int, age: int, weight: int, height: int, current_user=Depends(get_current_user)):
    
    if not current_user:
        raise HTTPException(status_code=401, detail="Authentication required")

    if select_athlete(athlete_id) != None:
        raise HTTPException(status_code=400, detail="Athlete already registered")
    
    new_athlete=insert_athlete(athlete_id=athlete_id, age=age, weight=weight, height=height)
    return {"message":"Athlete registered succesfully", "athlete":new_athlete}