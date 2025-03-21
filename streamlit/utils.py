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
    # POST request for authentification
    response = requests.post(f"{API_URL}/login?email={email}&password={password}")
    if response.status_code == 200:
        return response.json()  # Return the token in JSON format
    else:
        st.error("Fail to connect")
        return None

# Registration
def register_user(name:str, email: str, password: str, role: str):
    response = requests.post(f"{API_URL}/sign?name={name}&email={email}&password={password}&role={role}")
    if response.status_code == 200:
        return response.json()
    else:
        st.error("Fail to authentify.")
        return None
    
# Statistics
def fetch_data(endpoint):
    headers = {"Authorization": f"Bearer {st.session_state['token']}"}
    response = requests.get(f"{API_URL}/statistics/{endpoint}", headers=headers)
    if response.status_code == 200:
        return response.json().get("performances", "No available datas")
    else:
        return f"Error {response.status_code}: Error in fetch datas process."


def get_user_id_from_token():
    token = st.session_state.get("token")
    if not token:
        return None
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        user_id = payload.get("sub")
        return int(user_id)  
    except jwt.ExpiredSignatureError:
        st.error("Expired Session. Please reconnect.")
        return None
    except jwt.InvalidTokenError:
        st.error("Invalid token.")
        return None
    

def register_athlete(age:int, weight:int, height:int):

    if check_athlete_exists():
        st.warning("An athlete profil already exist with this profil.")
        return False
    user_id = get_user_id_from_token()
    if not user_id:
        st.error("Impossible to get user Id.")
        return False
    
    headers = {"Authorization": f"Bearer {st.session_state['token']}"}
    athlete_id = get_user_id_from_token()
    response = requests.post(f"{API_URL}/athlete/create?athlete_id={athlete_id}&age={age}&weight={weight}&height={height}", headers=headers)
    if response.status_code == 200:
        return True
    else:
        st.error(f"Erreur {response.status_code}: {response.text}")
        return False



def check_athlete_exists():
    """Check if an athlete exist or no"""
    
    user_id = get_user_id_from_token()
    if not user_id:
        return False
    
    headers = {"Authorization": f"Bearer {st.session_state['token']}"}
    response = requests.get(f"{API_URL}/athlete/{user_id}", headers=headers)

    if response.status_code == 200:
        return True  # Athlete exists
    return False  # Athele does not exist
