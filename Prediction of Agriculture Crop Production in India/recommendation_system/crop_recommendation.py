"""
Crop Recommendation System
Recommends best crops based on soil, weather, and environmental factors
"""

import numpy as np
import pandas as pd
from sklearn.preprocessing import LabelEncoder
import joblib
import os
from pathlib import Path
from typing import Dict

class CropRecommendation:
    def __init__(self):
        """Initialize crop recommendation system"""
        self.model_path = Path(__file__).parent.parent / 'models'
        self.crop_recommendations_db = {
            'Rice': {
                'temperature': (20, 30),
                'rainfall': (150, 300),
                'humidity': (70, 100),
                'soil_types': ['clayey', 'loamy'],
                'ph_range': (5.5, 7.5),
                'nutrients': {'N': 80, 'P': 40, 'K': 40}
            },
            'Wheat': {
                'temperature': (10, 25),
                'rainfall': (40, 100),
                'humidity': (30, 60),
                'soil_types': ['loamy', 'sandy loam'],
                'ph_range': (6.0, 7.0),
                'nutrients': {'N': 120, 'P': 60, 'K': 40}
            },
            'Maize': {
                'temperature': (15, 30),
                'rainfall': (60, 100),
                'humidity': (50, 75),
                'soil_types': ['loamy', 'sandy loam'],
                'ph_range': (5.8, 7.0),
                'nutrients': {'N': 150, 'P': 80, 'K': 60}
            },
            'Sugarcane': {
                'temperature': (20, 30),
                'rainfall': (100, 250),
                'humidity': (60, 85),
                'soil_types': ['loamy', 'clayey loam'],
                'ph_range': (6.0, 8.0),
                'nutrients': {'N': 200, 'P': 90, 'K': 90}
            },
            'Cotton': {
                'temperature': (21, 30),
                'rainfall': (60, 100),
                'humidity': (50, 70),
                'soil_types': ['black soil', 'sandy loam'],
                'ph_range': (6.0, 7.5),
                'nutrients': {'N': 100, 'P': 60, 'K': 40}
            },
            'Groundnut': {
                'temperature': (20, 30),
                'rainfall': (50, 100),
                'humidity': (40, 60),
                'soil_types': ['sandy', 'sandy loam'],
                'ph_range': (5.9, 7.0),
                'nutrients': {'N': 20, 'P': 50, 'K': 40}
            },
            'Soybean': {
                'temperature': (20, 30),
                'rainfall': (45, 100),
                'humidity': (50, 75),
                'soil_types': ['loamy', 'well-drained'],
                'ph_range': (6.0, 7.5),
                'nutrients': {'N': 0, 'P': 60, 'K': 40}  # Legume - fixes nitrogen
            }
        }
    
    def recommend_crop(self, temperature: float, rainfall: float, humidity: float, 
                      soil_type: str, ph: float, area: float, season: str):
        """
        Recommend crops based on environmental factors
        
        Args:
            temperature: Average temperature in Celsius
            rainfall: Annual rainfall in mm
            humidity: Average humidity percentage
            soil_type: Type of soil
            ph: Soil pH level
            area: Farm area in hectares
            season: Current season
        
        Returns:
            List with recommendations and confidence scores
        """
        recommendations = []
        
        for crop, requirements in self.crop_recommendations_db.items():
            score = 0
            reasons = []
            
            # Temperature check
            temp_min, temp_max = requirements['temperature']
            if temp_min <= temperature <= temp_max:
                score += 25
            elif abs(temperature - temp_min) < 3 or abs(temperature - temp_max) < 3:
                score += 15
                reasons.append(f"Temperature slightly outside optimal range")
            else:
                score -= 10
            
            # Rainfall check
            rain_min, rain_max = requirements['rainfall']
            if rain_min <= rainfall <= rain_max:
                score += 25
            elif abs(rainfall - rain_min) < 20 or abs(rainfall - rain_max) < 20:
                score += 15
                reasons.append(f"Rainfall slightly outside optimal range")
            else:
                score -= 10
            
            # Humidity check
            hum_min, hum_max = requirements['humidity']
            if hum_min <= humidity <= hum_max:
                score += 25
            else:
                score -= 5
            
            # Soil type check
            if soil_type.lower() in [s.lower() for s in requirements['soil_types']]:
                score += 15
            else:
                score += 5  # Still viable with amendments
                reasons.append(f"Soil type not ideal - may need amendments")
            
            # pH check
            ph_min, ph_max = requirements['ph_range']
            if ph_min <= ph <= ph_max:
                score += 10
            else:
                score -= 5
            
            # Ensure score is between 0-100
            score = max(0, min(100, score))
            
            if score > 30:  # Only recommend if score > 30%
                recommendations.append({
                    'crop': crop,
                    'confidence_score': score,
                    'reasons': reasons,
                    'required_nutrients': requirements['nutrients'],
                    'ideal_temperature': requirements['temperature'],
                    'ideal_rainfall': requirements['rainfall'],
                    'ideal_humidity': requirements['humidity']
                })
        
        # Sort by confidence score
        recommendations.sort(key=lambda x: x['confidence_score'], reverse=True)
        
        return {
            'top_recommendations': recommendations[:3],
            'all_recommendations': recommendations,
            'input_parameters': {
                'temperature': temperature,
                'rainfall': rainfall,
                'humidity': humidity,
                'soil_type': soil_type,
                'ph': ph,
                'area': area,
                'season': season
            }
        }
    
    def get_crop_info(self, crop_name: str) -> Dict:
        """Get detailed information about a crop"""
        if crop_name in self.crop_recommendations_db:
            return self.crop_recommendations_db[crop_name]
        return {}

# Initialize
crop_recommendation = CropRecommendation()
