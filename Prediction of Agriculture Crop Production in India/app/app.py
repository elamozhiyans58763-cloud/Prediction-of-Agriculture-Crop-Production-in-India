import os
import sys
import streamlit as st
import pandas as pd
import numpy as np

# Ensure current app directory is on sys.path for local imports when running with Streamlit
sys.path.append(os.path.dirname(__file__))
from prediction import crop_predictor
from utils import get_unique_values, load_dataset_preview, get_dataset_info
import matplotlib.pyplot as plt

# Page configuration
st.set_page_config(
    page_title="Crop Production Prediction",
    page_icon="🌾",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        color: #2E8B57;
        text-align: center;
        margin-bottom: 2rem;
    }
    .prediction-result {
        font-size: 1.5rem;
        font-weight: bold;
        color: #FF6347;
        text-align: center;
        padding: 1rem;
        border-radius: 10px;
        background-color: #F0F8FF;
        margin: 1rem 0;
    }
    .sidebar-header {
        font-size: 1.2rem;
        font-weight: bold;
        color: #4682B4;
        margin-bottom: 1rem;
    }
</style>
""", unsafe_allow_html=True)

def main():
    """
    Main function for the Streamlit application.
    """
    st.markdown('<h1 class="main-header">🌾 Crop Production Prediction System</h1>', unsafe_allow_html=True)
    st.markdown("Predict crop production in India based on agricultural and environmental factors using machine learning.")

    # Sidebar
    st.sidebar.markdown('<p class="sidebar-header">Navigation</p>', unsafe_allow_html=True)
    page = st.sidebar.radio("Choose a page:", ["Prediction", "Data Analysis", "Crop Recommendations", "About"])

    if page == "Prediction":
        show_prediction_page()
    elif page == "Data Analysis":
        show_data_analysis_page()
    elif page == "Crop Recommendations":
        show_recommendations_page()
    elif page == "About":
        show_about_page()

def show_prediction_page():
    """
    Display the main prediction page.
    """
    st.header("🌱 Crop Production Prediction")

    col1, col2 = st.columns([1, 1])

    with col1:
        st.subheader("Input Parameters")

        # Get unique values for dropdowns
        states = get_unique_values('State_Name')
        seasons = get_unique_values('Season')
        crops = get_unique_values('Crop')

        # Input fields
        state = st.selectbox("State", states if states else ["Maharashtra", "Karnataka", "Punjab"])
        district = st.text_input("District", "Pune")
        crop_year = st.number_input("Crop Year", min_value=2000, max_value=2030, value=2023)
        season = st.selectbox("Season", seasons if seasons else ["Kharif", "Rabi", "Whole Year"])
        crop = st.selectbox("Crop", crops if crops else ["Rice", "Wheat", "Maize"])
        area = st.number_input("Area (hectares)", min_value=0.1, value=10.0, step=0.1)
        rainfall = st.number_input("Annual Rainfall (mm)", min_value=0.0, value=1200.0, step=10.0)
        fertilizer = st.number_input("Fertilizer (kg/ha)", min_value=0.0, value=50.0, step=1.0)
        pesticide = st.number_input("Pesticide (kg/ha)", min_value=0.0, value=10.0, step=0.1)
        temperature = st.number_input("Temperature (°C)", min_value=0.0, value=25.0, step=0.1)

    with col2:
        st.subheader("Prediction Result")

        if st.button("Predict Production", type="primary"):
            # Prepare input data
            input_data = {
                'State_Name': state,
                'District_Name': district,
                'Crop_Year': crop_year,
                'Season': season,
                'Crop': crop,
                'Area': area,
                'Annual_Rainfall': rainfall,
                'Fertilizer': fertilizer,
                'Pesticide': pesticide,
                'Temperature': temperature
            }

            # Make prediction
            prediction = crop_predictor.predict(input_data)

            if prediction is not None:
                st.markdown(f'<div class="prediction-result">Predicted Production: {prediction:.2f} tons</div>', unsafe_allow_html=True)

                # Additional insights
                st.subheader("Additional Insights")

                # Fertilizer recommendation
                fertilizer_rec = crop_predictor.get_fertilizer_recommendation(crop, area)
                st.write("**Recommended Fertilizer (kg):**")
                st.json(fertilizer_rec)

                # Production category
                if prediction < 50:
                    category = "Low Production"
                    color = "🔴"
                elif prediction < 150:
                    category = "Medium Production"
                    color = "🟡"
                else:
                    category = "High Production"
                    color = "🟢"

                st.write(f"**Production Category:** {color} {category}")

            else:
                st.error("Prediction failed. Please check if the model is trained and available.")

def show_data_analysis_page():
    """
    Display the data analysis page with visualizations.
    """
    st.header("📊 Data Analysis & Visualizations")

    # Dataset preview
    st.subheader("Dataset Preview")
    preview_df = load_dataset_preview()
    if not preview_df.empty:
        st.dataframe(preview_df)
    else:
        st.warning("Dataset not found.")

    # Dataset info
    st.subheader("Dataset Information")
    info = get_dataset_info()
    if info:
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Number of Rows", info['shape'][0])
            st.metric("Number of Columns", info['shape'][1])
        with col2:
            st.write("**Columns:**")
            st.write(", ".join(info['columns']))

    # Visualizations
    st.subheader("Visualizations")
    plots = crop_predictor.get_visualizations()

    if plots:
        tab1, tab2, tab3, tab4 = st.tabs(["Production Trends", "Rainfall vs Production", "State Production", "Correlation"])

        with tab1:
            st.pyplot(plots['production_trends'])

        with tab2:
            st.pyplot(plots['rainfall_vs_production'])

        with tab3:
            st.pyplot(plots['state_production'])

        with tab4:
            st.pyplot(plots['correlation_heatmap'])
    else:
        st.warning("Unable to generate visualizations. Please check if the dataset is available.")

def show_recommendations_page():
    """
    Display the crop recommendations page.
    """
    st.header("🌾 Crop Recommendations")

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Input Conditions")

        states = get_unique_values('State_Name')
        seasons = get_unique_values('Season')

        state = st.selectbox("State", states if states else ["Maharashtra", "Karnataka", "Punjab"], key="rec_state")
        season = st.selectbox("Season", seasons if seasons else ["Kharif", "Rabi", "Whole Year"], key="rec_season")
        rainfall = st.number_input("Annual Rainfall (mm)", min_value=0.0, value=1200.0, step=10.0, key="rec_rainfall")
        temperature = st.number_input("Temperature (°C)", min_value=0.0, value=25.0, step=0.1, key="rec_temp")

    with col2:
        st.subheader("Recommendations")

        if st.button("Get Recommendations", key="rec_button"):
            recommendations = crop_predictor.get_crop_recommendations(state, season, rainfall, temperature)

            if recommendations:
                st.success("Recommended crops for your conditions:")
                for i, crop in enumerate(recommendations, 1):
                    st.write(f"{i}. {crop}")
            else:
                st.warning("No specific recommendations available for the given conditions.")

def show_about_page():
    """
    Display the about page.
    """
    st.header("ℹ️ About")

    st.markdown("""
    ## Crop Production Prediction System

    This application uses machine learning to predict crop production in India based on various agricultural and environmental factors.

    ### Features:
    - **Prediction**: Predict crop production using ML models
    - **Data Analysis**: Explore dataset with visualizations
    - **Recommendations**: Get crop and fertilizer recommendations
    - **Interactive UI**: User-friendly Streamlit interface

    ### Models Used:
    - Linear Regression
    - Random Forest Regressor
    - Decision Tree Regressor
    - XGBoost Regressor

    ### Dataset Features:
    - State and District information
    - Crop year and season
    - Area, rainfall, fertilizer, pesticide usage
    - Temperature and production data

    ### Technologies:
    - Python, Pandas, NumPy
    - Scikit-learn, XGBoost
    - Streamlit, Matplotlib, Seaborn
    """)

    st.markdown("---")
    st.markdown("**Developed for agricultural planning and decision making.**")

if __name__ == "__main__":
    main()