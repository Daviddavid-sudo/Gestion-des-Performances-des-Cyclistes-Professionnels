from fastapi import APIRouter, HTTPException, Depends
from core.security import get_current_user
from models.models import select_avg_power, select_max_weight_power_ratio, select_max_vo2


router =APIRouter(prefix="/statistics", tags=["statistics"])

@router.get("/maxpower")
async def max_power_performance(current_user=Depends(get_current_user)):
    """
    Endpoint to retrieve the maximum power performance of the current user.

    Args:
        current_user (User): The current authenticated user, obtained from the dependency injection.

    Raises:
        HTTPException: If the user is not authenticated (status code 401).

    Returns:
        dict: A dictionary containing the maximum power performances.
    """
    if not current_user:
        raise HTTPException(status_code=401, detail="Authentication required")

    recs = select_avg_power()
    return {"performances": recs}


@router.get("/maxvo2")
async def max_vo2_performance(current_user=Depends(get_current_user)):
    """
    Endpoint to retrieve the maximum VO2 performance records.

    This function requires user authentication. If the user is not authenticated,
    it raises an HTTP 401 Unauthorized error. Upon successful authentication, it
    retrieves the maximum VO2 performance records.

    Args:
        current_user: The current authenticated user, retrieved using dependency injection.

    Returns:
        dict: A dictionary containing the maximum VO2 performance records under the key 'performances'.

    Raises:
        HTTPException: If the user is not authenticated (status code 401).
    """
    if not current_user:
        raise HTTPException(status_code=401, detail="Authentication required")

    recs = select_max_vo2()
    return {"performances": recs}


@router.get("/maxweightratio")
async def max_weight_ratio_performance(current_user=Depends(get_current_user)):
    """
    Endpoint to get the maximum weight-to-power ratio performance for the current user.

    Args:
        current_user: The current authenticated user, obtained via dependency injection.

    Raises:
        HTTPException: If the user is not authenticated (status code 401).

    Returns:
        dict: A dictionary containing the maximum weight-to-power ratio performances.
    """
    if not current_user:
        raise HTTPException(status_code=401, detail="Authentication required")

    recs = select_max_weight_power_ratio()
    return {"performances": recs}