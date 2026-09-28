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
    page_icon="f4a295e4-0cba-4281-8d15-ba8833888662.png",
    layout="wide"
)


# -----------------------------
# CUSTOM UI / BACKGROUND
# -----------------------------

st.markdown("""
<style>

.stApp {
    background: linear-gradient(135deg, #e8f6ff 0%, #f4fbff 50%, #dff3f7 100%);
}

.main-title {
    text-align: center;
    font-size: 42px;
    font-weight: 800;
    margin-bottom: 0px;
}

.subtitle {
    text-align: center;
    font-size: 18px;
    color: #4a5a64;
    margin-bottom: 30px;
}

.section-card {
    background: rgba(255,255,255,0.85);
    padding: 25px;
    border-radius: 18px;
    margin-bottom: 20px;
    box-shadow: 0px 4px 15px rgba(0,0,0,0.08);
}

.guidance-card {
    background: rgba(255,255,255,0.9);
    padding: 22px;
    border-radius: 16px;
    margin-bottom: 18px;
    box-shadow: 0px 3px 12px rgba(0,0,0,0.07);
}

.footer {
    text-align: center;
    color: #60717c;
    font-size: 13px;
    margin-top: 35px;
}

</style>
""", unsafe_allow_html=True)


# -----------------------------
# LOAD MODEL
# -----------------------------

MODEL_PATH = "floodguard_ai_model_v2.pkl"

try:
    model = joblib.load(MODEL_PATH)

except Exception as e:
    st.error(f"Unable to load FloodGuard AI model: {e}")
    st.stop()


# -----------------------------
# HEADER
# -----------------------------

st.markdown(
    '<div class="main-title">🌧️ FloodGuard AI</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">AI-Powered Flood Risk Assessment & Preparedness</div>',
    unsafe_allow_html=True
)


# -----------------------------
# TWO TABS
# -----------------------------

tab1, tab2, tab3 = st.tabs([
    "🔍 Risk Assessment",
    "🛡️ Preparedness Guide",
    "📈 Data Analysis"
])


# =========================================================
# TAB 1 — RISK ASSESSMENT
# =========================================================

with tab1:

    st.markdown(
        '<div class="section-card">',
        unsafe_allow_html=True
    )

    st.header("📊 Environmental & Geographical Inputs")

    st.write(
        "Enter the environmental and geographical conditions "
        "to assess the modeled flood risk."
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

    st.markdown("</div>", unsafe_allow_html=True)


    # -----------------------------
    # ASSESS BUTTON
    # -----------------------------

    assess = st.button(
        "🌊 Assess Flood Risk",
        use_container_width=True
    )


    if assess:

        # IMPORTANT:
        # These column names MUST remain identical
        # to the names used while training the model.

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


        # -----------------------------
        # MODEL PREDICTION
        # -----------------------------

        try:

            prediction = model.predict(input_data)

            result = str(prediction[0])

            st.subheader("🌊 FloodGuard AI Assessment")


            if result.lower() in [
                "high",
                "high risk",
                "1"
            ]:

                st.error(
                    f"🚨 Flood Risk: {result}"
                )

            elif result.lower() in [
                "medium",
                "moderate",
                "medium risk"
            ]:

                st.warning(
                    f"⚠️ Flood Risk: {result}"
                )

            else:

                st.success(
                    f"✅ Flood Risk: {result}"
                )


            st.caption(
                "This assessment is generated by the trained "
                "FloodGuard AI model using the environmental and "
                "geographical conditions provided above."
            )


            # Save latest result for the Preparedness tab
            st.session_state["latest_prediction"] = result


        except Exception as e:

            st.error(
                f"Prediction error: {e}"
            )


# =========================================================
# TAB 2 — PREPAREDNESS GUIDE
# =========================================================

with tab2:

    st.header("🛡️ Flood Preparedness Guide")

    st.write(
        "Use the modeled risk level as a starting point for "
        "general preparedness. Always follow official warnings "
        "and instructions from local authorities."
    )


    # Get latest prediction if available
    latest_prediction = st.session_state.get(
        "latest_prediction",
        None
    )


    if latest_prediction is None:

        st.info(
            "🌊 Complete a Flood Risk Assessment in the first tab "
            "to view risk-based preparedness guidance."
        )

    else:

        result_lower = latest_prediction.lower()


        # =====================================================
        # HIGH RISK
        # =====================================================

        if result_lower in [
            "high",
            "high risk",
            "1"
        ]:

            st.error(
                f"🚨 Current Modeled Risk: {latest_prediction}"
            )

            st.markdown(
                '<div class="guidance-card">',
                unsafe_allow_html=True
            )

            st.subheader("✅ What to do")

            st.markdown("""
            - Monitor official weather and emergency communications.
            - Follow instructions issued by local authorities.
            - Keep essential emergency supplies easily accessible.
            - Keep important documents and essential items protected.
            - If local authorities issue an evacuation order, follow their instructions.
            """)

            st.markdown("</div>", unsafe_allow_html=True)


            st.markdown(
                '<div class="guidance-card">',
                unsafe_allow_html=True
            )

            st.subheader("⚠️ What to avoid")

            st.markdown("""
            - Do not enter or cross flooded areas.
            - Avoid rapidly flowing water.
            - Do not ignore official evacuation instructions.
            - Avoid unnecessary travel through areas affected by flooding.
            """)

            st.markdown("</div>", unsafe_allow_html=True)


        # =====================================================
        # MODERATE RISK
        # =====================================================

        elif result_lower in [
            "medium",
            "moderate",
            "medium risk"
        ]:

            st.warning(
                f"⚠️ Current Modeled Risk: {latest_prediction}"
            )

            st.markdown(
                '<div class="guidance-card">',
                unsafe_allow_html=True
            )

            st.subheader("✅ What to do")

            st.markdown("""
            - Monitor official weather and flood alerts.
            - Keep important documents and essential items protected.
            - Be prepared to follow local authority instructions.
            - Continue observing changes in rainfall and water conditions.
            """)

            st.markdown("</div>", unsafe_allow_html=True)


            st.markdown(
                '<div class="guidance-card">',
                unsafe_allow_html=True
            )

            st.subheader("⚠️ What to avoid")

            st.markdown("""
            - Avoid unnecessary exposure to potentially flooded areas.
            - Do not ignore worsening environmental conditions.
            - Do not ignore official weather or flood alerts.
            """)

            st.markdown("</div>", unsafe_allow_html=True)


        # =====================================================
        # LOW RISK
        # =====================================================

        else:

            st.success(
                f"✅ Current Modeled Risk: {latest_prediction}"
            )

            st.markdown(
                '<div class="guidance-card">',
                unsafe_allow_html=True
            )

            st.subheader("✅ Recommended preparedness")

            st.markdown("""
            - Continue monitoring local weather conditions.
            - Stay aware of official flood and weather alerts.
            - Keep important documents and essential items protected.
            - Remain prepared for changing environmental conditions.
            """)

            st.markdown("</div>", unsafe_allow_html=True)


            st.markdown(
                '<div class="guidance-card">',
                unsafe_allow_html=True
            )

            st.subheader("⚠️ Keep in mind")

            st.markdown("""
            - Do not assume conditions cannot change.
            - Do not ignore sudden increases in rainfall or water levels.
            - Follow official instructions if conditions change.
            """)

            st.markdown("</div>", unsafe_allow_html=True)

# =========================================================
# TAB 3 — DATA ANALYSIS
# =========================================================

with tab3:

    st.header("📈 Data Analysis")

    st.write(
        "Explore the relationships between rainfall and other "
        "numerical environmental factors present in the "
        "FloodGuard AI dataset."
    )

    try:

        graph_data = pd.read_csv("floodguard_dataset.csv")

        required_columns = [
            "Rainfall (mm)",
            "Temperature (degC)",
            "Humidity (%)",
            "River Discharge (m3/s)",
            "Water Level (m)",
            "Elevation (m)"
        ]

        missing_columns = [
            col for col in required_columns
            if col not in graph_data.columns
        ]

        if missing_columns:

            st.error(
                "The following required columns are missing "
                f"from the dataset: {missing_columns}"
            )

        else:

            st.subheader(
                "🌧️ Rainfall Relationships with Environmental Factors"
            )

            st.caption(
                "Each scatter plot shows how rainfall values "
                "are distributed in relation to another numerical "
                "environmental factor in the dataset."
            )

            fig, axes = plt.subplots(
                2,
                3,
                figsize=(15, 8)
            )

            relationships = [
                (
                    "Temperature (degC)",
                    "Temperature (°C)"
                ),
                (
                    "Humidity (%)",
                    "Humidity (%)"
                ),
                (
                    "River Discharge (m3/s)",
                    "River Discharge (m³/s)"
                ),
                (
                    "Water Level (m)",
                    "Water Level (m)"
                ),
                (
                    "Elevation (m)",
                    "Elevation (m)"
                )
            ]

            for ax, (column, label) in zip(
                axes.flat,
                relationships
            ):

                sns.scatterplot(
                    data=graph_data,
                    x="Rainfall (mm)",
                    y=column,
                    ax=ax,
                    alpha=0.6
                )

                ax.set_title(
                    f"Rainfall vs {label}"
                )

                ax.set_xlabel(
                    "Rainfall (mm)"
                )

                ax.set_ylabel(
                    label
                )

                ax.grid(
                    alpha=0.2
                )

            # Hide unused sixth plot
            axes[1, 2].axis("off")

            plt.tight_layout()

            st.pyplot(fig)

            st.info(
                "These visualizations are exploratory data analysis. "
                "They show relationships within the dataset and "
                "do not by themselves determine flood risk."
            )

    except FileNotFoundError:

        st.error(
            "Dataset file not found. Please add "
            "'floodguard_dataset.csv' to the same folder as app.py."
        )

    except Exception as e:

        st.error(
            f"Unable to generate the analysis graphs: {e}"
            )
# -----------------------------
# DISCLAIMER
# -----------------------------

st.markdown(
    '<div class="footer">'
    'FloodGuard AI provides a modeled flood-risk assessment and '
    'general preparedness guidance. It does not replace official '
    'weather warnings, emergency services, or instructions from '
    'local authorities.'
    '</div>',
    unsafe_allow_html=True
)

