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
# -----------------------------
# INPUT DATA
# -----------------------------

st.header("📊 Flood Risk Inputs")

col1, col2 = st.columns(2)

with col1:
    rainfall = st.number_input(
        "Rainfall (mm)",
        min_value=0.0,
        value=100.0,
        step=1.0
    )

    temperature = st.number_input(
        "Temperature (°C)",
        value=25.0,
        step=0.1
    )

    humidity = st.number_input(
        "Humidity (%)",
        min_value=0.0,
        max_value=100.0,
        value=70.0,
        step=1.0
    )

    river_discharge = st.number_input(
        "River Discharge",
        min_value=0.0,
        value=500.0,
        step=1.0
    )

with col2:
    water_level = st.number_input(
        "Water Level",
        min_value=0.0,
        value=5.0,
        step=0.1
    )

    elevation = st.number_input(
        "Elevation",
        min_value=0.0,
        value=100.0,
        step=1.0
    )

    land_cover = st.selectbox(
        "Land Cover",
        [
            "Forest",
            "Agricultural",
            "Urban",
            "Water Body",
            "Grassland"
        ]
    )

    soil_type = st.selectbox(
        "Soil Type",
        [
            "Sandy",
            "Clay",
            "Loamy",
            "Silty"
        ]
    )
    # -----------------------------
# PREDICTION
# -----------------------------

st.divider()

if st.button("🌊 Assess Flood Risk", use_container_width=True):

    input_data = pd.DataFrame({
        "Rainfall": [rainfall],
        "Temperature": [temperature],
        "Humidity": [humidity],
        "River Discharge": [river_discharge],
        "Water Level": [water_level],
        "Elevation": [elevation],
        "Land Cover": [land_cover],
        "Soil Type": [soil_type]
    })

    try:
        prediction = model.predict(input_data)

        st.subheader("FloodGuard AI Prediction")

        st.success(f"Prediction: {prediction[0]}")

    except Exception as e:
        st.error(f"Prediction error: {e}")
