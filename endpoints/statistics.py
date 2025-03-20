from fastapi import APIRouter, HTTPException, Depends
from core.security import get_current_user
from models.models import select_avg_power, select_max_weight_power_ratio, select_max_vo2


router =APIRouter(prefix="/statistics", tags=["statistics"])

@router.get("/maxpower")
async def max_power_performance(current_user=Depends(get_current_user)):
    if not current_user:
        raise HTTPException(status_code=401, detail="Authentication required")

    recs = select_avg_power()
    return {"performances": recs}


@router.get("/maxvo2")
async def max_vo2_performance(current_user=Depends(get_current_user)):
    if not current_user:
        raise HTTPException(status_code=401, detail="Authentication required")

    recs = select_max_vo2()
    return {"performances": recs}


@router.get("/maxweightratio")
async def max_weight_ratio_performance(current_user=Depends(get_current_user)):
    if not current_user:
        raise HTTPException(status_code=401, detail="Authentication required")

    recs = select_max_weight_power_ratio()
    return {"performances": recs}