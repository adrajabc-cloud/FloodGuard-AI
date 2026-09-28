import streamlit as st
import pandas as pd
import numpy as np
import joblib
import matplotlib.pyplot as plt
import seaborn as sns


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="FloodGuard AI",
    page_icon="floodguard_icon.png",
    layout="wide"
)


# ============================================================
# CUSTOM UI / BACKGROUND
# ============================================================

st.markdown(
    """
    <style>

    /* Main background */
    .stApp {
        background:
            radial-gradient(circle at 10% 10%, rgba(0, 170, 190, 0.16), transparent 28%),
            radial-gradient(circle at 90% 20%, rgba(30, 100, 180, 0.14), transparent 30%),
            linear-gradient(135deg, #eef9fc 0%, #f5fbfd 48%, #e8f5fa 100%);
    }

    /* Main content width */
    .block-container {
        padding-top: 2rem;
        padding-bottom: 3rem;
        max-width: 1200px;
    }

    /* Header */
    .flood-header {
        background: linear-gradient(
            135deg,
            rgba(8, 74, 102, 0.98),
            rgba(10, 128, 145, 0.95)
        );
        padding: 2rem 2.2rem;
        border-radius: 22px;
        margin-bottom: 1.8rem;
        box-shadow: 0 10px 30px rgba(0, 70, 100, 0.16);
    }

    .flood-header h1 {
        color: white;
        margin: 0;
        font-size: 2.5rem;
        font-weight: 750;
    }

    .flood-header p {
        color: rgba(255, 255, 255, 0.9);
        margin-top: 0.45rem;
        font-size: 1.05rem;
    }

    /* Section cards */
    .section-card {
        background: rgba(255, 255, 255, 0.86);
        padding: 1.35rem 1.5rem;
        border-radius: 18px;
        border: 1px solid rgba(0, 100, 130, 0.10);
        box-shadow: 0 6px 22px rgba(0, 60, 80, 0.07);
        margin-bottom: 1.3rem;
    }

    /* Result card */
    .result-card {
        background: rgba(255, 255, 255, 0.94);
        padding: 1.6rem;
        border-radius: 20px;
        border: 1px solid rgba(0, 100, 130, 0.12);
        box-shadow: 0 8px 28px rgba(0, 60, 80, 0.10);
        margin-top: 1rem;
    }

    /* Guidance cards */
    .guidance-card {
        background: rgba(255, 255, 255, 0.92);
        padding: 1.3rem 1.5rem;
        border-radius: 18px;
        border: 1px solid rgba(0, 100, 130, 0.10);
        margin-top: 1rem;
        box-shadow: 0 5px 18px rgba(0, 60, 80, 0.06);
    }

    .guidance-title {
        font-size: 1.2rem;
        font-weight: 700;
        margin-bottom: 0.6rem;
    }

    /* Footer */
    .footer {
        text-align: center;
        color: #52717c;
        font-size: 0.85rem;
        padding-top: 2rem;
    }

    </style>
    """,
    unsafe_allow_html=True
)


# ============================================================
# LOAD MODEL
# ============================================================

MODEL_PATH = "floodguard_ai_model_v2.pkl"

try:
    model = joblib.load(MODEL_PATH)

except Exception as e:
    st.error(f"Unable to load FloodGuard AI model: {e}")
    st.stop()


# ============================================================
# HEADER
# ============================================================

st.markdown(
    """
    <div class="flood-header">
        <h1>🌊 FloodGuard AI</h1>
        <p>
            AI-Powered Flood Risk Assessment & Community Preparedness
        </p>
    </div>
    """,
    unsafe_allow_html=True
)

st.write(
    "Enter the environmental and geographical conditions below "
    "to assess the modeled flood risk."
)


# ============================================================
# INPUT SECTION
# ============================================================

st.markdown(
    """
    <div class="section-card">
        <h3>📊 Environmental Conditions</h3>
        <p>
            Provide the conditions used by the FloodGuard AI model
            for its assessment.
        </p>
    </div>
    """,
    unsafe_allow_html=True
)

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
        "River Discharge (m³/s)",
        min_value=0.0,
        value=500.0,
        step=1.0
    )


with col2:

    water_level = st.number_input(
        "Water Level (m)",
        min_value=0.0,
        value=5.0,
        step=0.1
    )

    elevation = st.number_input(
        "Elevation (m)",
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


# ============================================================
# PREDICTION
# ============================================================

st.divider()

if st.button(
    "🌊 Assess Flood Risk",
    use_container_width=True
):

    input_data = pd.DataFrame({
        "Rainfall (mm)": [rainfall],
        "Temperature (degC)": [temperature],
        "Humidity (%)": [humidity],
        "River Discharge (m3/s)": [river_discharge],
        "Water Level (m)": [water_level],
        "Elevation (m)": [elevation],
        "Land Cover": [land_cover],
        "Soil Type": [soil_type]
    })

    try:

        prediction = model.predict(input_data)

        result = str(prediction[0])
        result_lower = result.lower()


        # ====================================================
        # RISK RESULT
        # ====================================================

        st.subheader("🌊 FloodGuard AI Assessment")


        if result_lower in ["high", "high risk", "1"]:

            st.error(
                f"🚨 HIGH FLOOD RISK\n\n"
                f"Model prediction: {result}"
            )

            guidance_title = "🛡️ High-Risk Preparedness"

            do_items = [
                "Monitor official emergency communications.",
                "Follow instructions issued by local authorities.",
                "Keep essential emergency supplies accessible.",
                "Move to a safer location if authorities advise evacuation."
            ]

            avoid_items = [
                "Do not enter or cross flooded areas.",
                "Avoid rapidly flowing water.",
                "Do not ignore official evacuation instructions."
            ]


        elif result_lower in [
            "medium",
            "moderate",
            "medium risk"
        ]:

            st.warning(
                f"⚠️ MODERATE FLOOD RISK\n\n"
                f"Model prediction: {result}"
            )

            guidance_title = "🛡️ Moderate-Risk Preparedness"

            do_items = [
                "Monitor official weather and flood alerts.",
                "Keep important documents and essential items protected.",
                "Be prepared to follow local authority instructions.",
                "Continue observing changing rainfall and water conditions."
            ]

            avoid_items = [
                "Avoid unnecessary exposure to potentially flooded areas.",
                "Do not ignore worsening conditions or official alerts."
            ]


        else:

            st.success(
                f"✅ LOW FLOOD RISK\n\n"
                f"Model prediction: {result}"
            )

            guidance_title = "🛡️ Low-Risk Preparedness"

            do_items = [
                "Continue monitoring local weather conditions.",
                "Stay aware of official flood and weather alerts.",
                "Keep important documents and essential items protected.",
                "Remain prepared for changing environmental conditions."
            ]

            avoid_items = [
                "Do not assume conditions cannot change.",
                "Do not ignore sudden increases in rainfall or water levels."
            ]


        # ====================================================
        # PREPAREDNESS GUIDANCE
        # ====================================================

        st.markdown(
            f"""
            <div class="guidance-card">
                <div class="guidance-title">
                    {guidance_title}
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

        guidance_col1, guidance_col2 = st.columns(2)


        with guidance_col1:

            st.markdown("### ✅ What to do")

            for item in do_items:
                st.markdown(f"- {item}")


        with guidance_col2:

            st.markdown("### ⚠️ What to avoid")

            for item in avoid_items:
                st.markdown(f"- {item}")


        # ====================================================
        # DISCLAIMER
        # ====================================================

        st.info(
            "FloodGuard AI provides a modeled flood-risk assessment "
            "and general preparedness guidance. It does not replace "
            "official weather warnings, emergency services, or "
            "instructions from local authorities."
        )


    except Exception as e:

        st.error(f"Prediction error: {e}")


# ============================================================
# FOOTER
# ============================================================

st.markdown(
    """
    <div class="footer">
        FloodGuard AI • AI-Based Flood Risk Assessment & Preparedness
    </div>
    """,
    unsafe_allow_html=True
)
