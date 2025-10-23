🧠 TIG Welding Heat Input Calculator & Predictor
📖 Overview

This Streamlit application allows users to calculate the heat input during a TIG (Tungsten Inert Gas) welding process and use a trained machine learning model to predict weld characteristics without requiring manual heat input entry.

Users can input welding parameters such as current, voltage, travel speed, and material type, and the app:

Automatically computes the heat input (J/mm),

Preprocesses the input values for model compatibility,

Predicts the desired welding output (like bead width, hardness, etc.), and

Displays both the calculated heat input and the prediction result interactively.

⚙️ Features

✅ Automatic Heat Input Calculation using the formula:

Heat Input (J/mm)
=
𝑉
×
𝐼
𝑆
×
60
Heat Input (J/mm)=
S
V×I
	​

×60

where:

𝑉
V = Voltage (Volts)

𝐼
I = Current (Amperes)

𝑆
S = Travel Speed (mm/s)

✅ Streamlit-based Interactive UI for easy data entry.
✅ Model Integration using a pre-trained RandomForestRegressor (or any regression model).
✅ Error Handling for missing or invalid inputs.
✅ Instant Predictions for real-time welding insights.

🧩 Tech Stack
Component	Technology
Frontend/UI	Streamlit
Backend	Python
ML Model	scikit-learn
Data Handling	pandas, numpy
Visualization	matplotlib / Streamlit components
