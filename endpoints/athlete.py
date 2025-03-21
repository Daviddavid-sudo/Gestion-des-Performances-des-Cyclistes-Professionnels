from fastapi import APIRouter, HTTPException, Depends, Request
from models.models import insert_athlete, select_athlete, delete_athlete, modify_athlete
from core.security import get_current_user

router =APIRouter(prefix="/athlete", tags=["athlete"])

@router.post("/create")
async def register_athlete(athlete_id: int, age: int, weight: int, height: int, current_user=Depends(get_current_user)):
    """
    Registers a new athlete.
    Args:
        athlete_id (int): The unique identifier for the athlete.
        age (int): The age of the athlete.
        weight (int): The weight of the athlete in kilograms.
        height (int): The height of the athlete in centimeters.
        current_user: The current authenticated user (injected by Depends).
    Raises:
        HTTPException: If the user is not authenticated (status code 401).
        HTTPException: If the athlete is already registered (status code 400).
    Returns:
        dict: A dictionary containing a success message and the newly registered athlete's details.
    """
    
    if not current_user:
        raise HTTPException(status_code=401, detail="Authentication required")

    if select_athlete(athlete_id) != None:
        raise HTTPException(status_code=400, detail="Athlete already registered")
    
    new_athlete=insert_athlete(athlete_id=athlete_id, age=age, weight=weight, height=height)
    return {"message":"Athlete registered succesfully", "athlete":new_athlete}

@router.post("/delete")
def deletion_athlete(athlete_id: int, current_user: dict = Depends(get_current_user)):
    """
    Deletes an athlete from the database.
    Args:
        athlete_id (int): The ID of the athlete to be deleted.
        current_user (dict, optional): The current authenticated user. Defaults to Depends(get_current_user).
    Raises:
        HTTPException: If the user is not authenticated.
        HTTPException: If the user does not have the 'coach' role.
        HTTPException: If the athlete does not exist.
    Returns:
        dict: A message indicating that the athlete was deleted successfully.
    """
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
    """
    Modify the details of an athlete.
    This endpoint allows an authenticated user to modify their athlete details.
    The user must be authenticated to access this endpoint.
    Args:
        request (Request): The HTTP request object.
        data (dict): The data to modify the athlete details.
        current_user (dict, optional): The current authenticated user. Defaults to Depends(get_current_user).
    Raises:
        HTTPException: If the user is not authenticated (status code 401).
    Returns:
        dict: The modified athlete details.
    """
    if not current_user:
        raise HTTPException(status_code=401, detail="Authentication required")
    
    data = await request.json()
    athlete_id = current_user.get('id')
    
    return modify_athlete(athlete_id=athlete_id, **data)