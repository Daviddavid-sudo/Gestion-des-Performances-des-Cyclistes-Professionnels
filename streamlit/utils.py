import streamlit as st
import requests
import jwt
from dotenv import load_dotenv
import os

load_dotenv()
API_URL=os.getenv("API_URL")
SECRET_KEY=os.getenv("SECRET_KEY")

# Authentification of user
def authenticate_user(email: str, password: str):
    """
    Authenticate a user by email and password.

    This function sends a POST request to the authentication endpoint 
    to verify user credentials and retrieve a JWT token if authentication is successful.

    ### Args:
        - `email` (str): The user's registered email.
        - `password` (str): The user's password.

    ### Returns:
        - `dict`: A JSON object containing the authentication token if successful.
        - `None`: If authentication fails.

    ### Raises:
        - Displays a Streamlit error message if authentication fails.

    Example Response:
    ```json
    {
        "access_token": "eyJhbGciOiJIUzI1NiIs...",
        "token_type": "bearer"
    }
    ```
    """
    response = requests.post(f"{API_URL}/login?email={email}&password={password}")
    if response.status_code == 200:
        return response.json()  # Return the token in JSON format
    else:
        st.error("Fail to connect")
        return None

# Registration
def register_user(name:str, email: str, password: str, role: str):
    """
    Register a new user.

    Sends a POST request to create a new user account with the given details.

    ### Args:
        - `name` (str): The user's full name.
        - `email` (str): The user's email address.
        - `password` (str): The password for the new account.
        - `role` (str): The role assigned to the user (e.g., "athlete", "coach").

    ### Returns:
        - `dict`: A JSON object confirming successful registration.
        - `None`: If registration fails.

    ### Raises:
        - Displays a Streamlit error message if registration fails.

    Example Response:
    ```json
    {
        "message": "User registered successfully"
    }
    ```
    """
    response = requests.post(f"{API_URL}/sign?name={name}&email={email}&password={password}&role={role}")
    if response.status_code == 200:
        return response.json()
    else:
        st.error("Fail to authentify.")
        return None
    
# Statistics
def fetch_data(endpoint):
    """
    Retrieve performance statistics from the API.

    This function fetches data from the given statistics endpoint.

    ### Args:
        - `endpoint` (str): The statistics endpoint to query (e.g., "maxpower", "maxvo2").

    ### Returns:
        - `dict`: The requested performance data if the request is successful.
        - `str`: An error message if the request fails.

    ### Raises:
        - Displays an error message in case of failure.

    Example Response:
    ```json
    {
        "performances": [
            {"athlete_id": 1, "max_power": 400, "date": "2025-03-20"},
            {"athlete_id": 2, "max_power": 390, "date": "2025-03-18"}
        ]
    }
    ```
    """
    headers = {"Authorization": f"Bearer {st.session_state['token']}"}
    response = requests.get(f"{API_URL}/statistics/{endpoint}", headers=headers)
    if response.status_code == 200:
        return response.json().get("performances", "No available datas")
    else:
        return f"Error {response.status_code}: Impossible to get datas."



def get_user_id_from_token():
    """
    Extract the user ID from the stored authentication token.

    This function retrieves the user ID by making a request to the `/users/me` endpoint.

    ### Returns:
        - `int`: The user ID if successfully retrieved.
        - `None`: If the token is invalid or the request fails.

    ### Raises:
        - Displays an error message if no token is found or if the request fails.

    Example Response:
    ```json
    {
        "id": 10,
        "name": "John Doe",
        "email": "johndoe@example.com"
    }
    ```
    """
    token = st.session_state.get("token")
    if not token:
        st.error("⚠️ No token found. Please log in.")
        return None

    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(f"{API_URL}/users/me", headers=headers)  # On demande l'ID au backend
    
    if response.status_code == 200:
        user_data = response.json()
        user_id = user_data.get("id")  
        print(f"get user id : {user_id}")  
        return user_id
    else:
        st.error(f"❌ Error {response.status_code}: {response.text}")
        return None


def register_athlete(age: int, weight: int, height: int):
    """
    Register an athlete's profile.

    This function checks if an athlete profile already exists for the logged-in user.
    If not, it sends a request to create a new athlete profile.

    ### Args:
        - `age` (int): The athlete's age.
        - `weight` (int): The athlete's weight in kg.
        - `height` (int): The athlete's height in cm.

    ### Returns:
        - `bool`: `True` if the athlete was registered successfully, `False` otherwise.

    ### Raises:
        - Displays an error message if the registration fails or if the user ID cannot be retrieved.

    Example Request:
    ```
    POST /athlete/create?athlete_id=10&age=25&weight=70&height=175
    ```
    """
    if check_athlete_exists():
        st.warning("An athlete profile already exists.")
        return False

    user_id = get_user_id_from_token()  # On récupère l'ID utilisateur
    if not user_id:
        st.error("Impossible to get user ID.")
        return False

    headers = {"Authorization": f"Bearer {st.session_state.get('token')}"}
    response = requests.post(f"{API_URL}/athlete/create?athlete_id={user_id}&age={age}&weight={weight}&height={height}", headers=headers)

    if response.status_code == 200:
        return True
    else:
        st.error(f"Erreur {response.status_code}: {response.text}")
        return False

def check_athlete_exists():
    """
    Check if an athlete profile already exists for the logged-in user.

    This function sends a request to verify whether the user has an associated athlete profile.

    ### Returns:
        - `bool`: `True` if an athlete profile exists, `False` otherwise.

    ### Raises:
        - Displays an error message if the user ID cannot be retrieved.

    Example Response:
    ```json
    {
        "athlete_id": 10,
        "age": 25,
        "weight": 70,
        "height": 175
    }
    ```
    """
    
    user_id = get_user_id_from_token()
    if not user_id:
        return False
    
    headers = {"Authorization": f"Bearer {st.session_state['token']}"}
    response = requests.get(f"{API_URL}/athlete/{user_id}", headers=headers)

    if response.status_code == 200:
        return True  # Athlete exists
    return False  # Athlete does not exist
