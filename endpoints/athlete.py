from core.security import get_password_hash
from fastapi import APIRouter, HTTPException, Depends, Request
from models.models import insert_athlete, select_athlete, delete_athlete, modify_athlete
from core.security import get_current_user

router =APIRouter(prefix="/athlete", tags=["athlete"])

@router.post("/create")
async def register_athlete(athlete_id: int, age: int, weight: int, height: int, current_user=Depends(get_current_user)):
    
    if not current_user:
        raise HTTPException(status_code=401, detail="Authentication required")

    if select_athlete(athlete_id) != None:
        raise HTTPException(status_code=400, detail="Athlete already registered")
    
    new_athlete=insert_athlete(athlete_id=athlete_id, age=age, weight=weight, height=height)
    return {"message":"Athlete registered succesfully", "athlete":new_athlete}

@router.post("/delete")
def deletion_athlete(athlete_id: int, current_user: dict = Depends(get_current_user)):
    print("Current User:", current_user)
    if not current_user:
        raise HTTPException(status_code=401, detail="Authentication required")
    
    if current_user['role'] != 'coach':
        raise HTTPException(status_code=401, detail="You don't have the right to delete this account, contact your coach")

    if select_athlete(athlete_id) == None:
        raise HTTPException(status_code=400, detail="Athlete does not exist")
    
    delete_athlete(athlete_id=athlete_id)
    
    return {"message":"Athlete deleted successfully"}

@router.put("/modify")
async def modification_athlete(request: Request, data=dict, current_user: dict = Depends(get_current_user)):
    if not current_user:
        raise HTTPException(status_code=401, detail="Authentication required")
    
    data = await request.json()
    athlete_id = current_user.get('id')
    
    return modify_athlete(athlete_id=athlete_id, **data)