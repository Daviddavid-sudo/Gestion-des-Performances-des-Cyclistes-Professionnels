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
        return f"Error {response.status_code}: Impossible to get datas."



def get_user_id_from_token():
    """Get the user id by the token """
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
    """Check if an athlete exists for the logged-in user"""
    
    user_id = get_user_id_from_token()
    if not user_id:
        return False
    
    headers = {"Authorization": f"Bearer {st.session_state['token']}"}
    response = requests.get(f"{API_URL}/athlete/{user_id}", headers=headers)

    if response.status_code == 200:
        return True  # Athlete exists
    return False  # Athlete does not exist
