import streamlit as st 
from utils import register_athlete, check_athlete_exists


st.title("📝 Register your personal information")
if check_athlete_exists():
    st.warning("You have already register your personal informations")
    st.stop()

age = st.number_input("age", min_value=0, max_value=100)
weight= st.number_input("weight (kg)", min_value=0, max_value=200)
height = st.number_input("height (cm)", min_value=49, max_value=250)

if st.button("Register"):
    result = register_athlete(age, weight, height)
    if result:
        st.success("Your account has been created. You can login.")

