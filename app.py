import streamlit as st
import pandas as pd
import joblib
from PIL import Image
import matplotlib.pyplot as plt
import seaborn as sns
import urllib.request

# Set page config
st.set_page_config(
    page_title="CO₂ Predictor",
    page_icon="🌿",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Load the trained model
@st.cache_resource
def load_model():
    try:
        # Replace with your Google Drive direct download link
        url = "https://drive.google.com/uc?export=download&id=19lyMxgVSDg05qscSSUClIlbTvOvP3sBK"
        filename, _ = urllib.request.urlretrieve("co2_emission_predictor_rf.pkl")
        return joblib.load(filename)
    except Exception as e:
        st.error(f"Error loading model: {e}")
        return None

model = load_model()

# App header
st.title("🚗 CO₂ Emission Predictor")
st.markdown("""
Estimate your vehicle's CO₂ emissions based on basic specifications. 
This tool helps you understand your environmental impact when choosing a vehicle.
""")

# Sidebar with information
with st.sidebar:
    st.header("About This Tool")
    st.markdown("""
    This predictive model estimates CO₂ emissions (in grams per kilometer) based on:
    - Vehicle model year
    - Fuel type
    - Kilometers driven
    - Engine size
    - Transmission type
    
    The model was trained on realistic vehicle data with emissions calculated considering:
    - Age degradation effects
    - Mileage impact
    - Fuel type differences
    - Engine size scaling
    """)
    
    st.markdown("---")
    st.markdown("**Project by:** Abdul Hadi (L1S22BSCS0351)")
    st.markdown("**Course:** BSCS - Introductiion to Data Science")

# Main content
col1, col2 = st.columns([1, 1])

with col1:
    st.subheader("Vehicle Specifications")
    
    # Create form for user input
    with st.form("prediction_form"):
        # Model Year
        model_year = st.slider(
            "Model Year",
            min_value=1985,
            max_value=2025,
            value=2018,
            help="Select your vehicle's manufacturing year"
        )
        
        # Fuel Type
        fuel_type = st.selectbox(
            "Fuel Type",
            options=["Petrol", "Diesel", "Hybrid", "Electric"],
            index=0,
            help="Select your vehicle's fuel type"
        )
        
        # Kilometers Driven
        kms_driven = st.number_input(
            "Kilometers Driven",
            min_value=0,
            max_value=500000,
            value=50000,
            step=1000,
            help="Enter total kilometers the vehicle has been driven"
        )
        
        # Engine Size
        engine_cc = st.selectbox(
            "Engine Size (cc)",
            options=[1000, 1200, 1500, 1800, 2000, 2200, 2500, 2800, 3000, 3200, 3500, 3800, 4000, 4500, 5000],
            index=4,
            help="Select your vehicle's engine displacement"
        )
        
        # Transmission Type
        transmission = st.radio(
            "Transmission Type",
            options=["Manual", "Automatic"],
            index=0,
            horizontal=True
        )
        
        # Submit button
        submitted = st.form_submit_button("Calculate CO₂ Emissions", type="primary")

with col2:
    st.subheader("Prediction Results")
    
    if submitted:
        # Create input dataframe
        input_data = pd.DataFrame({
            'Model_Year': [model_year],
            'Fuel_Type': [fuel_type],
            'KMs_Driven': [kms_driven],
            'Engine_CC': [engine_cc],
            'Transmission_Type': [transmission]
        })
        
        # Make prediction
        prediction = model.predict(input_data)[0]
        
        # Display result
        if fuel_type == "Electric":
            st.success("## 🎉 0 g/km")
            st.markdown("Electric vehicles produce zero direct CO₂ emissions!")
        else:
            # Color code based on emission level
            if prediction < 100:
                emission_color = "green"
                emission_icon = "✅"
                emission_message = "Low Emissions"
            elif prediction < 180:
                emission_color = "orange"
                emission_icon = "⚠️"
                emission_message = "Moderate Emissions"
            else:
                emission_color = "red"
                emission_icon = "❌"
                emission_message = "High Emissions"
            
            st.markdown(f"""
            <div style='background-color:#f0f2f6; padding:20px; border-radius:10px;'>
                <h2 style='color:{emission_color}; text-align:center;'>
                    {emission_icon} {prediction:.1f} g/km
                </h2>
                <p style='text-align:center; font-size:18px;'>{emission_message}</p>
            </div>
            """, unsafe_allow_html=True)
            
            # Emission comparison
            st.markdown("### How does this compare?")
            
            comparison_data = {
                "Vehicle Type": ["Small Petrol Car", "Average Diesel Car", "SUV", "Your Vehicle"],
                "CO₂ Emissions (g/km)": [120, 150, 200, prediction]
            }
            
            fig, ax = plt.subplots(figsize=(8, 4))
            sns.barplot(
                x="Vehicle Type",
                y="CO₂ Emissions (g/km)",
                data=pd.DataFrame(comparison_data),
                palette=["#1f77b4", "#1f77b4", "#1f77b4", emission_color],
                ax=ax
            )
            ax.set_title("Emission Comparison")
            st.pyplot(fig)
            
            # Tips for reducing emissions
            if prediction > 150:
                st.warning("**Tips to reduce emissions:**")
                st.markdown("""
                - Consider more frequent maintenance
                - Check tire pressure regularly
                - Reduce unnecessary weight in vehicle
                - Consider a more efficient vehicle for your next purchase
                """)

# Additional information section
st.markdown("---")
st.subheader("Understanding Your Results")

col_info1, col_info2, col_info3 = st.columns(3)

with col_info1:
    st.markdown("""
    **Emission Standards Reference:**
    - Euro 6 (2021): 95 g/km (average for new cars)
    - Euro 5 (2009): 130 g/km
    - Euro 4 (2005): 160 g/km
    """)

with col_info2:
    st.markdown("""
    **Typical Emissions by Fuel:**
    - Petrol: 120-200 g/km
    - Diesel: 100-180 g/km
    - Hybrid: 50-120 g/km
    - Electric: 0 g/km (direct)
    """)

with col_info3:
    st.markdown("""
    **Factors Affecting Emissions:**
    - Older vehicles typically emit more
    - Higher mileage increases emissions
    - Larger engines produce more CO₂
    - Automatic transmissions often less efficient
    """)

# Add some styling
st.markdown("""
<style>
    .stSlider>div>div>div>div {
        background: #1f77b4;
    }
    .st-b7 {
        background-color: #1f77b4;
    }
    .st-c0 {
        background-color: #1f77b4;
    }
</style>
""", unsafe_allow_html=True)
