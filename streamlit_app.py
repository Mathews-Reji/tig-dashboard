import streamlit as st
import joblib
import numpy as np
import pandas as pd

# ------------------------------
# Load trained model pipeline
# ------------------------------
model = joblib.load("tig_random_forest_pipeline.pkl")

st.set_page_config(page_title="TIG Welding Hardness Predictor", page_icon="⚙️")
st.title("TIG Welding Hardness & Heat Predictor")

st.markdown("""
This app predicts **hardness (HRC)** and calculates **heat input (J/mm)** 
for TIG welded Aluminium Alloy specimens based on your process parameters.
""")

# ------------------------------
# Input Section
# ------------------------------
col1, col2 = st.columns(2)

with col1:
    tig_type = st.selectbox("Weld Type", ["Normal", "TiC Powdered"])
    groove = st.selectbox("Groove Type", ["No Groove", "Groove"])
    voltage = st.number_input("Voltage (V)", min_value=0.0, value=100.0)
    ampere = st.number_input("Current (A)", min_value=0.0, value=100.0)

with col2:
    travel_speed = st.number_input("Travel Speed (mm/s)", min_value=0.1, value=2.0)
    bead_width = st.number_input("Bead Width (mm)", min_value=0.1, value=2.5)

# ------------------------------
# Feature Preparation
# ------------------------------
heat_input = (voltage * ampere * 60) / (travel_speed + 1e-6)  # J/mm

input_data = pd.DataFrame([{
    "Type": tig_type,
    "Groove": groove,
    "Voltage (V)": voltage,
    "Current (A)": ampere,
    "Travel_Speed (mm/s)": travel_speed,
    "Bead_Width (mm)": bead_width,
    "heat_input_J_per_mm": heat_input
}])

# ------------------------------
# Prediction
# ------------------------------
if st.button("🔍 Predict Hardness"):
    hardness_pred = model.predict(input_data)[0]
    st.success(f"**Predicted Hardness:** {hardness_pred:.2f} HRC")
    st.info(f"**Calculated Heat Input:** {heat_input:.2f} J/mm")

    st.caption("Note: Heat input is a calculated parameter, not predicted by the model.")

# ------------------------------
# Extra Info
# ------------------------------
st.divider()
st.markdown("""
### ℹ️ Model Details
- Algorithm: Random Forest Regressor  
- Input Features: TIG Type, Groove, Voltage, Ampere, Travel Speed, Bead Width  
- Target: Hardness (HRC100)  
- Derived: Heat Input (J/mm)
""")
