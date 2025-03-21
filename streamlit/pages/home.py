import streamlit as st

st.set_page_config(page_title="Home", page_icon="🏠")

if "authenticated" not in st.session_state or not st.session_state["authenticated"]:
    st.error("Please login first")
    st.stop()

st.title("🏠 Welcome to the Cyclist app. Check your performance!")

st.write("What do you want to do ?")

# Navigation menu
if st.button("See the datas"):
    st.switch_page("pages/data.py")

if st.button("Enter your personal informations"):
    st.switch_page("pages/athlete.py")

if st.button("Modify your personal informations"):
    st.switch_page("pages/athlete_creation.py")
