from fastapi import APIRouter, HTTPException, Depends
from core.security import get_current_user
from models.models import select_performance, insert_performance, modify_performance, delete_performance, select_performance, select_all_performance, get_role


router =APIRouter(prefix="/performance", tags=["performance"])

@router.post("/create")
async def register_performance(vo2max: int, hr: int, rf: int, cadence: int, ppo: int, completion_date: str,current_user=Depends(get_current_user)):
    """
    Registers a new performance for the current user.
    Args:
        vo2max (int): The VO2 max value of the athlete.
        hr (int): The heart rate of the athlete.
        rf (int): The respiratory frequency of the athlete.
        cadence (int): The cadence of the athlete.
        ppo (int): The peak power output of the athlete.
        completion_date (str): The date when the performance was completed.
        current_user: The current authenticated user (automatically provided by Depends).
    Raises:
        HTTPException: If the user is not authenticated (status code 401).
        HTTPException: If the athlete is already registered (status code 400).
    Returns:
        dict: A message indicating that the performance was registered successfully.
    """
    if not current_user:
        raise HTTPException(status_code=401, detail="Authentication required")
    
    athlete_id = current_user["id"]
    if select_performance(athlete_id) != None:
        raise HTTPException(status_code=400, detail="Athlete already registered")
    
    new_athlete=insert_performance(athlete_id=athlete_id, vo2max=vo2max, hr=hr, rf=rf, cadence=cadence, ppo=ppo, completion_date=completion_date)
    return {"message":"Performance registered succesfully"}


@router.post("/update")
def update_performance(performance_id: int, athlete_id: int,vo2max: int, hr: int, rf: int, cadence: int, ppo: int, completion_date: str, current_user=Depends(get_current_user)):
    """
    Update the performance metrics for a given athlete.

    Args:
        performance_id (int): The ID of the performance record to update.
        athlete_id (int): The ID of the athlete whose performance is being updated.
        vo2max (int): The VO2 max value of the athlete.
        hr (int): The heart rate of the athlete.
        rf (int): The respiratory frequency of the athlete.
        cadence (int): The cadence of the athlete.
        ppo (int): The peak power output of the athlete.
        completion_date (str): The date when the performance was completed.
        current_user: The current authenticated user (default is obtained from Depends(get_current_user)).

    Raises:
        HTTPException: If the user is not authenticated (status code 401).

    Returns:
        dict: A message indicating that the performance was updated successfully.
    """
    if not current_user:
        raise HTTPException(status_code=401, detail="Authentication required")

    modify_performance(performance_id=performance_id, athlete_id=athlete_id, vo2max=vo2max, hr=hr, rf=rf, cadence=cadence, ppo=ppo, completion_date=completion_date)
    return {"message":"Performance updated succesfully"}


@router.post("/delete")
def remove_performance(performance_id: int, current_user=Depends(get_current_user)):
    """
    Remove a performance record by its ID.

    Args:
        performance_id (int): The ID of the performance to be removed.
        current_user: The current authenticated user, obtained via dependency injection.

    Raises:
        HTTPException: If the user is not authenticated (status code 401).

    Returns:
        dict: A message indicating that the performance was successfully removed.
    """
    if not current_user:
        raise HTTPException(status_code=401, detail="Authentication required")

    delete_performance(performance_id=performance_id)
    return {"message":"Performance succesfully removed"}


@router.get("/select")
def history_everyone_performance(current_user=Depends(get_current_user)):
    """
    Retrieve performance history for all users if the current user is an admin,
    otherwise retrieve performance history for the current user.

    Args:
        current_user (dict): The current authenticated user obtained from the dependency injection.

    Raises:
        HTTPException: If the user is not authenticated (status code 401).

    Returns:
        dict: A dictionary containing the performance records. If the user is an admin,
              it returns performance records for all users. Otherwise, it returns performance
              records for the current user.
    """
    if not current_user:
        raise HTTPException(status_code=401, detail="Authentication required")
    id = current_user["id"]
    role = get_role(id=id)
    print(role)
    if role == "admin":
        recs = select_all_performance()
        return {"performances": recs}
    else:
        athlete_id = current_user["id"]
        recs = select_performance(athlete_id=athlete_id)
        return {"performances": recs}