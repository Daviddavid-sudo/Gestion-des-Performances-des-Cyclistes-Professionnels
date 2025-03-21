import streamlit as st
import datetime
import requests
from utils import authenticate_user, register_user



st.set_page_config(page_title="Cyclists Data App", page_icon="🚴")

# Menu pour basculer entre Connexion et Inscription
menu = st.sidebar.selectbox("Menu", ["Login", "Sign up"])

if menu == "Login":
    st.title("🔑 Login")
    email = st.text_input("email")
    password = st.text_input("password", type="password")
    
    if st.button("Login"):
        user_data = authenticate_user(email, password)
        if user_data:
            st.success("You are connected !")
            st.session_state["authenticated"] = True
            st.session_state["token"] = user_data["access_token"]
            st.switch_page("pages/home.py")  # Redirect to home page

elif menu == "Sign up":
    st.title("📝 Registration")
    name = st.text_input("name")
    email = st.text_input("email")
    password = st.text_input("password", type="password")
    role = st.selectbox("Choose your role :", ("athlete", "coach"))
    
    if st.button("Create your account"):
        result = register_user(name, email, password, role)
        if result:
            st.success("Your account has been created. You can login.")

