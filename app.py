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
    page_icon="f4a295e4-0cba-4281-8d15-ba8833888662.png",
    layout="wide",
    initial_sidebar_state="collapsed"
)


# ============================================================
# CUSTOM FLOODGUARD AI STYLING
# ============================================================

st.markdown("""
<style>

    /* ---------- APP BACKGROUND ---------- */

    .stApp {
        background-color: #f4f9fc;
    }

    .block-container {
        padding-top: 1.5rem;
        padding-bottom: 2rem;
        max-width: 1400px;
    }


    /* ---------- HEADER ---------- */

    .brand-header {
        background: linear-gradient(
            135deg,
            #e8f7ff 0%,
            #f8fcff 55%,
            #e6f7f5 100%
        );

        border: 1px solid #c7e5f5;
        border-radius: 18px;
        padding: 1.5rem 1.8rem;
        margin-bottom: 1.2rem;
        box-shadow: 0 4px 18px rgba(15, 76, 92, 0.08);
    }

    .brand-title {
        font-size: 2.7rem;
        font-weight: 800;
        color: #073b73;
        margin: 0;
    }

    .brand-ai {
        color: #079bd8;
    }

    .brand-subtitle {
        font-size: 1.05rem;
        font-weight: 600;
        color: #315b78;
        margin-top: 0.3rem;
    }

    .brand-motto {
        color: #52748b;
        font-size: 0.95rem;
        margin-top: 0.45rem;
    }


    /* ---------- SECTION HEADINGS ---------- */

    .section-title {
        font-size: 1.45rem;
        font-weight: 750;
        color: #084c75;
        margin-top: 0.5rem;
        margin-bottom: 0.3rem;
    }

    .section-description {
        color: #536b7a;
        margin-bottom: 1rem;
    }


    /* ---------- CARDS ---------- */

    .info-card {
        background: white;
        border: 1px solid #d5e8f2;
        border-radius: 15px;
        padding: 1.2rem 1.4rem;
        margin-bottom: 1rem;
        box-shadow: 0 3px 12px rgba(15, 76, 92, 0.06);
    }

    .card-title {
        font-size: 1.15rem;
        font-weight: 700;
        color: #0b5275;
        margin-bottom: 0.4rem;
    }


    /* ---------- PREPAREDNESS CARDS ---------- */

    .prep-card {
        background: white;
        border: 1px solid #d5e8f2;
        border-left: 5px solid #0891b2;
        border-radius: 12px;
        padding: 1.1rem 1.3rem;
        margin-bottom: 1rem;
        box-shadow: 0 3px 10px rgba(15, 76, 92, 0.05);
    }

    .prep-title {
        color: #075985;
        font-size: 1.15rem;
        font-weight: 700;
        margin-bottom: 0.5rem;
    }


    /* ---------- FOOTER ---------- */

    .footer {
        text-align: center;
        color: #647b89;
        font-size: 0.82rem;
        padding-top: 1.5rem;
        margin-top: 2rem;
        border-top: 1px solid #d5e8f2;
    }


    /* ---------- BUTTON ---------- */

    div.stButton > button {
        width: 100%;
        border-radius: 10px;
        font-weight: 700;
        min-height: 3rem;
    }


    /* ---------- TABS ---------- */

    button[data-baseweb="tab"] {
        font-size: 1.05rem;
        font-weight: 650;
    }

</style>
""", unsafe_allow_html=True)


# ============================================================
# LOAD TRAINED MODEL
# ============================================================

MODEL_PATH = "floodguard_ai_model_v2.pkl"

try:
    model = joblib.load(MODEL_PATH)

except Exception as e:
    st.error(f"Unable to load FloodGuard AI model: {e}")
    st.stop()


# ============================================================
# FLOODGUARD HEADER
# ============================================================

st.markdown("""
<div class="brand-header">

    <div class="brand-title">
        🌊 FloodGuard <span class="brand-ai">AI</span>
    </div>

    <div class="brand-subtitle">
        AI-Powered Flood Risk Assessment & Community Preparedness
    </div>

    <div class="brand-motto">
        Predict&nbsp;&nbsp; • &nbsp;&nbsp;Understand&nbsp;&nbsp; • &nbsp;&nbsp;Prepare
    </div>

</div>
""", unsafe_allow_html=True)


# ============================================================
# TWO MAIN TABS
# ============================================================

risk_tab, preparedness_tab = st.tabs(
    [
        "🌊  Risk Assessment",
        "🛡️  Flood Preparedness"
    ]
)


# ============================================================
# TAB 1 — RISK ASSESSMENT
# ============================================================

with risk_tab:

    st.markdown(
        '<div class="section-title">'
        '📊 Environmental & Geographical Inputs'
        '</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="section-description">'
        'Enter the current or hypothetical environmental conditions '
        'to generate a FloodGuard AI assessment.'
        '</div>',
        unsafe_allow_html=True
    )

    col1, col2 = st.columns(2)


    # --------------------------------------------------------
    # LEFT COLUMN
    # --------------------------------------------------------

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


    # --------------------------------------------------------
    # RIGHT COLUMN
    # --------------------------------------------------------

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


    # --------------------------------------------------------
    # ASSESS BUTTON
    # --------------------------------------------------------

    st.write("")

    if st.button(
        "🌊  Assess Flood Risk",
        use_container_width=True,
        type="primary"
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


            # ------------------------------------------------
            # ASSESSMENT
            # ------------------------------------------------

            st.divider()

            st.markdown(
                '<div class="section-title">'
                '🧠 FloodGuard AI Assessment'
                '</div>',
                unsafe_allow_html=True
            )


            if result.lower() in ["high", "high risk", "1"]:

                st.error(
                    f"🚨 Flood Risk: {result}"
                )

                preparedness_message = """
                **Preparedness focus:** Conditions indicate elevated
                predicted flood risk. Monitor official warnings,
                avoid unnecessary travel through flood-prone areas,
                and keep essential emergency supplies accessible.
                """


            elif result.lower() in [
                "medium",
                "moderate",
                "medium risk"
            ]:

                st.warning(
                    f"⚠️ Flood Risk: {result}"
                )

                preparedness_message = """
                **Preparedness focus:** Continue monitoring local
                weather and flood conditions. Keep emergency contacts,
                essential supplies and evacuation information ready.
                """


            else:

                st.success(
                    f"✅ Flood Risk: {result}"
                )

                preparedness_message = """
                **Preparedness focus:** Current input conditions
                indicate lower predicted flood risk. Continue normal
                monitoring, especially during periods of heavy rainfall.
                """


            # ------------------------------------------------
            # WHAT THIS MEANS
            # ------------------------------------------------

            st.markdown("""
            <div class="info-card">

                <div class="card-title">
                    💡 What This Means
                </div>

                FloodGuard AI has evaluated the environmental and
                geographical conditions provided above using the
                trained machine-learning model.

            </div>
            """, unsafe_allow_html=True)


            # ------------------------------------------------
            # PREPAREDNESS
            # ------------------------------------------------

            st.markdown(
                f"""
                <div class="prep-card">

                    <div class="prep-title">
                        🛡️ Community Preparedness
                    </div>

                    {preparedness_message}

                </div>
                """,
                unsafe_allow_html=True
            )


            # ------------------------------------------------
            # DISCLAIMER
            # ------------------------------------------------

            st.caption(
                "This assessment is generated by the trained "
                "FloodGuard AI model using the environmental and "
                "geographical conditions provided above. It is "
                "intended for educational and preparedness purposes "
                "and should not replace official emergency warnings."
            )


        except Exception as e:

            st.error(
                f"Prediction error: {e}"
            )


# ============================================================
# TAB 2 — FLOOD PREPAREDNESS
# ============================================================

with preparedness_tab:

    st.markdown(
        '<div class="section-title">'
        '🛡️ Flood Preparedness Centre'
        '</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="section-description">'
        'FloodGuard AI is not only about assessing risk — '
        'preparedness helps communities respond effectively.'
        '</div>',
        unsafe_allow_html=True
    )


    # --------------------------------------------------------
    # BEFORE A FLOOD
    # --------------------------------------------------------

    st.markdown("""
    <div class="prep-card">

        <div class="prep-title">
            🏠 Before a Flood
        </div>

        <ul>
            <li>Monitor weather forecasts and official alerts.</li>
            <li>Keep emergency contacts easily accessible.</li>
            <li>Prepare essential medicines, food, water and
                important documents.</li>
            <li>Know the safest evacuation route from your area.</li>
            <li>Keep emergency supplies in an easily accessible
                location.</li>
        </ul>

    </div>
    """, unsafe_allow_html=True)


    # --------------------------------------------------------
    # DURING A FLOOD
    # --------------------------------------------------------

    st.markdown("""
    <div class="prep-card">

        <div class="prep-title">
            🌧️ During a Flood
        </div>

        <ul>
            <li>Follow instructions from local authorities.</li>
            <li>Move to safer or higher locations when advised.</li>
            <li>Avoid walking or driving through floodwater.</li>
            <li>Stay informed through reliable official channels.</li>
            <li>Keep communication devices charged whenever possible.</li>
        </ul>

    </div>
    """, unsafe_allow_html=True)


    # --------------------------------------------------------
    # AFTER A FLOOD
    # --------------------------------------------------------

    st.markdown("""
    <div class="prep-card">

        <div class="prep-title">
            🌱 After a Flood
        </div>

        <ul>
            <li>Return only when authorities indicate that it is safe.</li>
            <li>Avoid potentially contaminated water.</li>
            <li>Be cautious around damaged buildings and infrastructure.</li>
            <li>Report hazards to the appropriate local authorities.</li>
            <li>Continue monitoring official updates.</li>
        </ul>

    </div>
    """, unsafe_allow_html=True)


    # --------------------------------------------------------
    # EMERGENCY KIT
    # --------------------------------------------------------

    st.markdown("""
    <div class="info-card">

        <div class="card-title">
            🎒 Emergency Preparedness Kit
        </div>

        <p>
        A basic emergency kit can include:
        </p>

        <ul>
            <li>Drinking water and non-perishable food</li>
            <li>First-aid supplies</li>
            <li>Flashlight and spare batteries</li>
            <li>Essential medicines</li>
            <li>Important documents stored safely</li>
            <li>Charged communication devices / power bank</li>
        </ul>

    </div>
    """, unsafe_allow_html=True)


    # --------------------------------------------------------
    # COMMUNITY PREPAREDNESS
    # --------------------------------------------------------

    st.markdown("""
    <div class="info-card">

        <div class="card-title">
            🤝 Community Preparedness
        </div>

        <p>
        Flood resilience improves when individuals and communities
        prepare together.
        </p>

        <ul>
            <li>Share reliable flood alerts with vulnerable neighbours.</li>
            <li>Know local evacuation and shelter information.</li>
            <li>Help identify people who may need additional assistance.</li>
            <li>Participate in local preparedness activities.</li>
            <li>Rely on official emergency information during disasters.</li>
        </ul>

    </div>
    """, unsafe_allow_html=True)


    # --------------------------------------------------------
    # FLOODGUARD MESSAGE
    # --------------------------------------------------------

    st.success(
        "🌊 FloodGuard AI: Predict → Understand → Prepare"
    )

    st.caption(
        "FloodGuard AI is an educational project designed to "
        "demonstrate how machine learning can support flood-risk "
        "awareness and community preparedness."
    )


# ============================================================
# FOOTER
# ============================================================

st.markdown("""
<div class="footer">

    <b>🌊 FloodGuard AI</b>
    &nbsp; • &nbsp;
    AI for Flood Risk Awareness & Preparedness

    <br><br>

    Predict &nbsp;•&nbsp; Understand &nbsp;•&nbsp; Prepare

</div>
""", unsafe_allow_html=True)
