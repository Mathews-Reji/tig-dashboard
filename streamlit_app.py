import streamlit as st
import joblib
import numpy as np
import pandas as pd

# Load the model
model = joblib.load("random_forest_model.pkl")

st.title("TIG Welding Hardness Predictor")

# User inputs
tig_type = st.selectbox("TIG Weld Type", ["Normal", "TiC Powdered"])
voltage = st.number_input("Voltage (V)", min_value=0.0, value=100.0)
ampere = st.number_input("Current (A)", min_value=0.0, value=100.0)
bead_width = st.number_input("Bead Width (mm)", min_value=0.1, value=2.5)

# Encode tig_weld
tig_encoded = 0 if tig_type == "Normal" else 1

# Calculate heat
heat = (voltage * ampere * 60) / (1000 * (bead_width + 1e-6))

# Predict button
if st.button("Predict Hardness"):
    input_data = pd.DataFrame([[tig_encoded, voltage, ampere, bead_width, heat]],
                              columns=["tig_weld", "voltage", "ampere", "bead_width", "heat"])
    pred = model.predict(input_data)[0]
    st.success(f"Predicted Hardness (HRC100): {pred:.2f}")
