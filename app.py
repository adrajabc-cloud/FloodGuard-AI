import streamlit as st
import pandas as pd
import numpy as np
import joblib
import matplotlib.pyplot as plt
import seaborn as sns


# -----------------------------
# PAGE CONFIGURATION
# -----------------------------

st.set_page_config(
    page_title="FloodGuard AI",
    page_icon="🌊",
    layout="wide"
)


# -----------------------------
# LOAD TRAINED MODEL
# -----------------------------

MODEL_PATH = "floodguard_ai_model_v2.pkl"

try:
    model = joblib.load(MODEL_PATH)
except Exception as e:
    st.error(f"Unable to load FloodGuard AI model: {e}")
    st.stop()


# -----------------------------
# FLOODGUARD AI
# -----------------------------

st.title("🌊 FloodGuard AI")
st.subheader("AI-Powered Flood Risk Assessment")

st.write(
    "Enter the environmental and geographical conditions below "
    "to assess the predicted flood risk."
)
