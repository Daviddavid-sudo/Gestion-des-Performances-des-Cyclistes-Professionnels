from fastapi import APIRouter, HTTPException, Depends
from fastapi.responses import JSONResponse
from core.security import verify_password, create_access_token, get_password_hash, get_current_user, OAuth2PasswordBearer
from models.models import select_user, select_performance, insert_performance, modify_performance, delete_performance


router =APIRouter(prefix="/performance", tags=["performance"])

@router.post("/create")
async def register_performance(vo2max: int, hr: int, rf: int, cadence: int, ppo: int, completion_date: str,current_user=Depends(get_current_user)):
    if not current_user:
        raise HTTPException(status_code=401, detail="Authentication required")
    
    athlete_id = current_user["id"]
    if select_performance(athlete_id) != None:
        raise HTTPException(status_code=400, detail="Athlete already registered")
    
    new_athlete=insert_performance(athlete_id=athlete_id, vo2max=vo2max, hr=hr, rf=rf, cadence=cadence, ppo=ppo, completion_date=completion_date)
    return {"message":"Performance registered succesfully"}


@router.post("/update")
def update_performance(performance_id: int, athlete_id: int,vo2max: int, hr: int, rf: int, cadence: int, ppo: int, completion_date: str, current_user=Depends(get_current_user)):
    if not current_user:
        raise HTTPException(status_code=401, detail="Authentication required")

    modify_performance(performance_id=performance_id, athlete_id=athlete_id, vo2max=vo2max, hr=hr, rf=rf, cadence=cadence, ppo=ppo, completion_date=completion_date)
    return {"message":"Performance updated succesfully"}

@router.post("/delete")
def remove_performance(performance_id: int, current_user=Depends(get_current_user)):
    if not current_user:
        raise HTTPException(status_code=401, detail="Authentication required")

    delete_performance(performance_id=performance_id)
    return {"message":"Performance succesfully removed"}