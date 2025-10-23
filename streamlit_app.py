import streamlit as st
import pandas as pd
import numpy as np
import joblib
import urllib.request
import os

# ------------------------------
# Title and description
# ------------------------------
st.set_page_config(page_title="TIG Welding Hardness Predictor", page_icon="⚙️", layout="centered")
st.title("🧠 TIG Welding Hardness & Heat Predictor")
st.write("Predict TIG weld hardness (HRC) and calculate heat input based on your parameters.")

# ------------------------------
# Step 1: Load trained pipeline model
# ------------------------------
MODEL_URL = "https://github.com/Mathews-Reji/tig-dashboard/raw/main/tig_random_forest_model.pkl"
MODEL_PATH = "tig_random_forest_model.pkl"

if not os.path.exists(MODEL_PATH):
    with st.spinner("Downloading model..."):
        urllib.request.urlretrieve(MODEL_URL, MODEL_PATH)
        st.success("✅ Model downloaded successfully!")

# Load model (which includes the preprocessor)
model = joblib.load(MODEL_PATH)

# ------------------------------
# Step 2: Collect input parameters
# ------------------------------
st.subheader("🔧 Enter Welding Parameters")

col1, col2 = st.columns(2)

with col1:
    current = st.number_input("Current (A)", min_value=10.0, max_value=300.0, value=120.0)
    voltage = st.number_input("Voltage (V)", min_value=5.0, max_value=50.0, value=15.0)
    travel_speed = st.number_input("Travel Speed (mm/s)", min_value=0.1, max_value=20.0, value=5.0)
with col2:
    bead_width = st.number_input("Bead Width (mm)", min_value=0.5, max_value=20.0, value=5.0)
    # Add placeholders for the categorical columns used in training
    type_ = st.selectbox("Weld Type", ["Type1", "Type2", "Type3"])
    powder = st.selectbox("Powder", ["PowderA", "PowderB", "PowderC"])
    groove = st.selectbox("Groove", ["GrooveA", "GrooveB", "GrooveC"])
    tic = st.selectbox("TIC", ["Yes", "No"])
    method = st.selectbox("Method", ["TIG", "TIG-Pulse", "MIG"])

# ------------------------------
# Step 3: Build input DataFrame
# ------------------------------
# ⚠️ The column names here must match EXACTLY those used during training
input_dict = {
    "Current (A)": current,
    "Voltage (V)": voltage,
    "Travel_Speed (mm/s)": travel_speed,
    "Bead_Width (mm)": bead_width,
    "Type": type_,
    "Powder": powder,
    "Groove": groove,
    "TIC": tic,
    "Method": method
}

input_df = pd.DataFrame([input_dict])

# ------------------------------
# Step 4: Predict hardness & calculate heat
# ------------------------------
if st.button("🔍 Predict Hardness"):
    try:
        hardness_pred = model.predict(input_df)[0]
        heat_input = (voltage * current * 60) / (1000 * travel_speed)

        st.success(f"**Predicted Hardness (HRC):** {hardness_pred:.2f}")
        st.info(f"**Calculated Heat Input:** {heat_input:.2f} J/mm")

        st.write("---")
        st.write("### Input Summary")
        st.dataframe(input_df)

    except Exception as e:
        st.error(f"❌ Error during prediction: {e}")

# ------------------------------
# Footer
# ------------------------------
st.markdown(
    """
    ---
    🔬 Developed by **Mathews Reji**  
    Built using **Streamlit + Scikit-Learn**
    """
)
