import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

# Ensure app directory is on sys.path when imported as a module
app_dir = os.path.dirname(__file__)
import sys
if app_dir not in sys.path:
    sys.path.append(app_dir)

from utils import prediction_utils, load_dataset_preview, get_dataset_info

class CropPredictor:
    """
    Class for handling crop production predictions and visualizations.
    """

    def __init__(self):
        """
        Initialize the crop predictor.
        """
        self.utils = prediction_utils

    def predict(self, input_data):
        """
        Make a prediction based on input data.

        Args:
            input_data (dict): Input features for prediction

        Returns:
            float: Predicted production value
        """
        return self.utils.predict_production(input_data)

    def get_visualizations(self):
        """
        Generate visualizations for the dataset.

        Returns:
            dict: Dictionary containing plot figures
        """
        try:
            df = pd.read_csv('../dataset/crop_production.csv')

            plots = {}

            # Crop production trends
            fig1, ax1 = plt.subplots(figsize=(10, 6))
            yearly_prod = df.groupby('Crop_Year')['Production'].sum()
            ax1.plot(yearly_prod.index, yearly_prod.values, marker='o', color='blue')
            ax1.set_title('Crop Production Trends Over Years')
            ax1.set_xlabel('Year')
            ax1.set_ylabel('Total Production')
            ax1.grid(True)
            plots['production_trends'] = fig1

            # Rainfall vs Production
            fig2, ax2 = plt.subplots(figsize=(10, 6))
            ax2.scatter(df['Annual_Rainfall'], df['Production'], alpha=0.5, color='green')
            ax2.set_title('Rainfall vs Production')
            ax2.set_xlabel('Annual Rainfall (mm)')
            ax2.set_ylabel('Production')
            ax2.grid(True)
            plots['rainfall_vs_production'] = fig2

            # State-wise production (top 10)
            fig3, ax3 = plt.subplots(figsize=(12, 6))
            state_prod = df.groupby('State_Name')['Production'].sum().sort_values(ascending=False).head(10)
            state_prod.plot(kind='bar', ax=ax3, color='orange')
            ax3.set_title('Top 10 States by Total Production')
            ax3.set_xlabel('State')
            ax3.set_ylabel('Total Production')
            ax3.tick_params(axis='x', rotation=45)
            plots['state_production'] = fig3

            # Correlation heatmap
            fig4, ax4 = plt.subplots(figsize=(10, 8))
            numerical_cols = ['Crop_Year', 'Area', 'Annual_Rainfall', 'Fertilizer', 'Pesticide', 'Temperature', 'Production']
            corr_matrix = df[numerical_cols].corr()
            sns.heatmap(corr_matrix, annot=True, cmap='coolwarm', center=0, ax=ax4)
            ax4.set_title('Correlation Heatmap')
            plots['correlation_heatmap'] = fig4

            return plots

        except FileNotFoundError:
            st.error("Dataset not found. Please ensure the dataset is available.")
            return {}

    def get_crop_recommendations(self, state, season, rainfall, temperature):
        """
        Provide crop recommendations based on conditions.
        This is a simple rule-based system.

        Args:
            state (str): State name
            season (str): Season
            rainfall (float): Annual rainfall
            temperature (float): Temperature

        Returns:
            list: List of recommended crops
        """
        recommendations = []

        # Simple rule-based recommendations
        if season == 'Kharif':
            if rainfall > 1500:
                recommendations.extend(['Rice', 'Sugarcane', 'Jute'])
            elif rainfall > 1000:
                recommendations.extend(['Rice', 'Maize', 'Cotton'])
            else:
                recommendations.extend(['Maize', 'Cotton'])
        elif season == 'Rabi':
            if temperature < 20:
                recommendations.extend(['Wheat', 'Barley', 'Mustard'])
            else:
                recommendations.extend(['Wheat', 'Sugarcane', 'Potato'])
        else:  # Whole Year
            recommendations.extend(['Coconut', 'Sugarcane'])

        # State-specific recommendations (simplified)
        state_specific = {
            'Punjab': ['Wheat', 'Rice', 'Cotton'],
            'Maharashtra': ['Sugarcane', 'Cotton', 'Soybean'],
            'Karnataka': ['Rice', 'Ragi', 'Sugarcane'],
            'Uttar Pradesh': ['Wheat', 'Rice', 'Sugarcane']
        }

        if state in state_specific:
            recommendations.extend(state_specific[state])

        # Remove duplicates and return top recommendations
        return list(set(recommendations))[:5]

    def get_fertilizer_recommendation(self, crop, area):
        """
        Provide fertilizer recommendations based on crop and area.

        Args:
            crop (str): Crop name
            area (float): Area in hectares

        Returns:
            dict: Fertilizer recommendations
        """
        # Simplified fertilizer recommendations (kg per hectare)
        fertilizer_guide = {
            'Rice': {'Nitrogen': 120, 'Phosphorus': 60, 'Potassium': 40},
            'Wheat': {'Nitrogen': 100, 'Phosphorus': 50, 'Potassium': 50},
            'Maize': {'Nitrogen': 150, 'Phosphorus': 75, 'Potassium': 60},
            'Cotton': {'Nitrogen': 100, 'Phosphorus': 50, 'Potassium': 50},
            'Sugarcane': {'Nitrogen': 250, 'Phosphorus': 100, 'Potassium': 100}
        }

        if crop in fertilizer_guide:
            base_rec = fertilizer_guide[crop]
            # Scale by area
            scaled_rec = {k: v * area for k, v in base_rec.items()}
            return scaled_rec
        else:
            # Default recommendation
            return {'Nitrogen': 100 * area, 'Phosphorus': 50 * area, 'Potassium': 50 * area}

# Global instance
crop_predictor = CropPredictor()