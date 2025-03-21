import streamlit as st
import requests
from utils import fetch_data



# Check the authentification
if "authenticated" not in st.session_state or not st.session_state["authenticated"]:
    st.error("Please login first.")
    st.stop()

st.set_page_config(page_title="Statistiques des Performances", page_icon="📈")

st.title("📊 Statistics")

st.subheader("⚡ Maximum average power")
max_power = fetch_data("maxpower")
st.write(max_power)

st.subheader("🫁 Maximum VO2")
max_vo2 = fetch_data("maxvo2")
st.write(max_vo2)

st.subheader("⚖ Maximum Power/Weight Ratio")
max_weight_ratio = fetch_data("maxweightratio")
st.write(max_weight_ratio)
