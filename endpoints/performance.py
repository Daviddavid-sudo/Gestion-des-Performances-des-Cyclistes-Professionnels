from fastapi import APIRouter, HTTPException, Depends
from fastapi.responses import JSONResponse
from core.security import verify_password, create_access_token, get_password_hash, get_current_user, OAuth2PasswordBearer
from models.models import select_user, select_performance, insert_performance
import datetime

# router= APIRouter(tags=['performance'])


# request_scheme = OAuth2PasswordBearer(tokenUrl="endpoints/connexion/login")

# @router.post("/performance")
# async def add_performance(vo2max,hr,rf,cadence,PPO, token: str = Depends(request_scheme)):
#     completion_date=datetime.time.now()
#     current_user = get_current_user(token)
#     return {"current_user":current_user}
#     # user_id = select_user(email)
#     # if not user or not verify_password(password, get_password_hash(password)):
#     #      raise HTTPException(status_code=400, detail="Invalid credentials")
#     # access_token = create_access_token(data={"sub": email})

#     # return  {"email": email, "access_token": access_token}


router =APIRouter(prefix="/performance", tags=["performance"])

@router.post("/create")
async def register_user(vo2max: int, hr: int, rf: int, cadence: int, ppo: int, completion_date: str,current_user=Depends(get_current_user)):
    if not current_user:
        raise HTTPException(status_code=401, detail="Authentication required")
    
    athlete_id = current_user["id"]
    if select_performance(athlete_id) != None:
        raise HTTPException(status_code=400, detail="Athlete already registered")
    
    new_athlete=insert_performance(athlete_id=athlete_id, vo2max=vo2max, hr=hr, rf=rf, cadence=cadence, ppo=ppo, commpletion_date=completion_date)
    return {"message":"Athlete registered succesfully", "athlete":new_athlete}