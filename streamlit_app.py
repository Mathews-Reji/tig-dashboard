import streamlit as st
import pandas as pd
import numpy as np
import joblib
import urllib.request
import os

# ------------------------------
# Page configuration
# ------------------------------
st.set_page_config(page_title="TIG Welding Hardness Predictor", page_icon="⚙️", layout="centered")
st.title("🧠 TIG Welding Hardness & Heat Predictor")
st.write("Predict hardness (HRC) and calculate heat input (J/mm) for TIG welding parameters.")

# ------------------------------
# Step 1: Load trained model
# ------------------------------
MODEL_URL = "https://github.com/Mathews-Reji/tig-dashboard/raw/main/tig_random_forest_model.pkl"
MODEL_PATH = "tig_random_forest_model.pkl"

if not os.path.exists(MODEL_PATH):
    with st.spinner("Downloading trained Random Forest model..."):
        urllib.request.urlretrieve(MODEL_URL, MODEL_PATH)
        st.success("✅ Model downloaded successfully!")

try:
    model = joblib.load(MODEL_PATH)
except Exception as e:
    st.error(f"❌ Failed to load model: {e}")
    st.stop()

# ------------------------------
# Step 2: Input fields
# ------------------------------
st.subheader("🔧 Enter Welding Parameters")

col1, col2 = st.columns(2)

with col1:
    voltage = st.number_input("Voltage (V)", min_value=5.0, max_value=50.0, value=15.0)
    current = st.number_input("Current (A)", min_value=10.0, max_value=300.0, value=120.0)

with col2:
    travel_speed = st.number_input("Travel Speed (mm/s)", min_value=0.1, max_value=20.0, value=5.0)
    bead_width = st.number_input("Bead Width (mm)", min_value=0.5, max_value=20.0, value=5.0)

# ------------------------------
# Step 3: Prepare input
# ------------------------------
# Construct DataFrame with the same structure as training data
input_dict = {
    "Voltage (V)": voltage,
    "Current (A)": current,
    "Travel_Speed (mm/s)": travel_speed,
    "Bead_Width (mm)": bead_width
}

input_df = pd.DataFrame([input_dict])

# Calculate heat input (as per your training code)
input_df["heat_input_J_per_mm"] = (input_df['Voltage (V)'] * input_df['Current (A)'] * 60) / (input_df['Travel_Speed (mm/s)'] + 1e-6)

# ------------------------------
# Step 4: Predict hardness
# ------------------------------
if st.button("🔍 Predict Hardness"):
    try:
        prediction = model.predict(input_df)[0]
        heat_input = input_df["heat_input_J_per_mm"].iloc[0]

        st.success(f"**Predicted Hardness (HRC):** {prediction:.2f}")
        st.info(f"**Calculated Heat Input:** {heat_input:.2f} J/mm")

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
    Built using **Streamlit + Scikit-Learn (Random Forest)**  
    """
)
