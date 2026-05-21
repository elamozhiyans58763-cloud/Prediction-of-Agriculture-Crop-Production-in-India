"""
AI Chatbot for Farmers
Provides agricultural advice and recommendations
"""

import json
from typing import Dict, List
import re

class FarmerChatbot:
    def __init__(self):
        """Initialize chatbot with knowledge base"""
        self.knowledge_base = {
            'greetings': {
                'hello': 'Hello! Welcome to the Smart Agriculture System. How can I help you today?',
                'hi': 'Hi there! I\'m here to help with your farming needs. What would you like to know?',
                'hey': 'Hey! Ask me about crops, diseases, fertilizers, or irrigation.',
            },
            'crop_info': {
                'rice': 'Rice is a monsoon crop. It needs high rainfall (150-300mm), waterlogged conditions, and temperatures between 20-30°C. Ideal for clayey soil.',
                'wheat': 'Wheat is a winter crop (Rabi). It needs temperatures between 10-25°C, moderate rainfall (40-100mm), and well-drained loamy soil.',
                'maize': 'Maize needs 15-30°C temperature, 60-100mm rainfall, and good drainage. Plant in Kharif or summer season.',
                'sugarcane': 'Sugarcane is a long-duration crop needing 20-30°C temperature and 100-250mm rainfall. Needs rich soil with good organic matter.',
                'cotton': 'Cotton needs 21-30°C temperature, 60-100mm rainfall, and well-drained black soil or sandy loam.',
            },
            'disease_info': {
                'blight': 'Leaf blight causes brown/black spots on leaves. Treatment: Apply fungicide, improve air circulation, remove infected leaves.',
                'rust': 'Rust shows orange/red powdery spores. Treatment: Apply sulfur or copper-based fungicide, ensure plant spacing.',
                'mildew': 'Powdery mildew causes white powdery coating. Treatment: Apply sulfur dust, improve ventilation, avoid excess nitrogen.',
                'bacterial': 'Bacterial spot shows small dark spots with yellow halos. Treatment: Apply copper bactericide, improve drainage.',
            },
            'fertilizer_info': {
                'nitrogen': 'Nitrogen promotes leaf and stem growth. Good sources: Urea, Ammonium Sulfate. Apply in split doses.',
                'phosphorus': 'Phosphorus promotes flowering and root development. Good sources: DAP, SSP. Apply at sowing time.',
                'potassium': 'Potassium improves disease resistance and crop quality. Good sources: MOP, KNO3. Apply during growth.',
            },
            'irrigation_info': {
                'rice': 'Rice needs 4-5 irrigations. Keep field flooded during main season. Total: 1000-1200mm water.',
                'wheat': 'Wheat needs 4 irrigations. First at CRI (Crown Root Initiation), then at flowering and grain filling.',
                'maize': 'Maize needs 4-5 irrigations. Critical stages: 25-50 days and 70-90 days after sowing.',
            },
            'seasonal_advice': {
                'kharif': 'Kharif season (June-October): Best for rice, maize, cotton, groundnut. Prepare soil, use quality seeds.',
                'rabi': 'Rabi season (October-March): Best for wheat, gram, mustard. Ensure good soil moisture at sowing.',
                'summer': 'Summer season (March-June): Plan for summer crops, prepare irrigation, apply mulch.',
            }
        }
    
    def process_input(self, user_input: str) -> str:
        """
        Process user input and generate response
        
        Args:
            user_input: User's question or statement
        
        Returns:
            Chatbot response
        """
        # Convert to lowercase for matching
        user_input_lower = user_input.lower()
        
        # Check for greetings
        for greeting, response in self.knowledge_base['greetings'].items():
            if greeting in user_input_lower:
                return response
        
        # Check for crop information
        for crop, info in self.knowledge_base['crop_info'].items():
            if crop in user_input_lower:
                return f"📌 {crop.upper()}: {info}"
        
        # Check for disease information
        for disease, info in self.knowledge_base['disease_info'].items():
            if disease in user_input_lower:
                return f"🦠 DISEASE - {disease.upper()}: {info}"
        
        # Check for fertilizer information
        for nutrient, info in self.knowledge_base['fertilizer_info'].items():
            if nutrient in user_input_lower:
                return f"🌱 NUTRIENT - {nutrient.upper()}: {info}"
        
        # Check for irrigation information
        for crop, info in self.knowledge_base['irrigation_info'].items():
            if crop in user_input_lower:
                return f"💧 IRRIGATION - {crop.upper()}: {info}"
        
        # Check for seasonal advice
        for season, advice in self.knowledge_base['seasonal_advice'].items():
            if season in user_input_lower:
                return f"📅 {season.upper()} SEASON: {advice}"
        
        # If no match found, provide helpful suggestions
        return self.get_suggestions()
    
    def get_suggestions(self) -> str:
        """Get list of available topics"""
        suggestions = """
I can help you with:

🌾 CROPS: Ask about rice, wheat, maize, sugarcane, cotton, groundnut, soybean
🦠 DISEASES: Ask about blight, rust, mildew, bacterial spot, early blight
🧪 FERTILIZERS: Ask about nitrogen, phosphorus, potassium recommendations
💧 IRRIGATION: Ask about water requirements for different crops
📅 SEASONS: Ask about Kharif, Rabi, and Summer season cultivation

Example questions:
- "Tell me about rice cultivation"
- "How to treat leaf blight?"
- "What's the fertilizer for wheat?"
- "When to irrigate cotton?"
- "Tips for Kharif season"

What would you like to know?
        """
        return suggestions
    
    def get_crop_advice(self, crop: str, season: str):
        """Get comprehensive advice for a crop"""
        advice = {
            'crop': crop,
            'season': season,
            'planting_time': self._get_planting_time(crop, season),
            'soil_requirements': self._get_soil_requirements(crop),
            'water_requirements': self._get_water_requirements(crop),
            'nutrient_requirements': self._get_nutrient_requirements(crop),
            'common_diseases': self._get_common_diseases(crop),
            'harvest_time': self._get_harvest_time(crop, season),
            'expected_yield': self._get_expected_yield(crop)
        }
        return advice
    
    def _get_planting_time(self, crop: str, season: str) -> str:
        """Get planting time for crop"""
        timing = {
            ('rice', 'kharif'): 'June-July (Monsoon onset)',
            ('wheat', 'rabi'): 'October-November',
            ('maize', 'kharif'): 'April-May',
            ('cotton', 'kharif'): 'April-May',
            ('groundnut', 'kharif'): 'May-June',
        }
        return timing.get((crop.lower(), season.lower()), 'Check local climate')
    
    def _get_soil_requirements(self, crop: str) -> str:
        """Get soil requirements"""
        soils = {
            'rice': 'Clayey, waterlogged, pH 5.5-7.5',
            'wheat': 'Well-drained loamy, pH 6.0-7.0',
            'maize': 'Loamy, fertile, pH 5.8-7.0',
            'cotton': 'Black soil, sandy loam, pH 6.0-7.5',
            'groundnut': 'Sandy loam, well-drained, pH 5.9-7.0',
        }
        return soils.get(crop.lower(), 'Fertile, well-drained soil')
    
    def _get_water_requirements(self, crop: str) -> str:
        """Get water requirements"""
        water = {
            'rice': '1000-1200 mm (flooded)',
            'wheat': '450-600 mm',
            'maize': '500-600 mm',
            'cotton': '650-850 mm',
            'groundnut': '400-500 mm',
        }
        return water.get(crop.lower(), '500-800 mm')
    
    def _get_nutrient_requirements(self, crop: str) -> str:
        """Get nutrient requirements"""
        nutrients = {
            'rice': 'N:80-100, P:40-50, K:40-50 kg/ha',
            'wheat': 'N:120-150, P:60-80, K:40-60 kg/ha',
            'maize': 'N:150-200, P:80-100, K:60-80 kg/ha',
            'cotton': 'N:100-120, P:60-80, K:40-60 kg/ha',
            'groundnut': 'N:20-25, P:50-60, K:40-50 kg/ha',
        }
        return nutrients.get(crop.lower(), 'Balanced NPK')
    
    def _get_common_diseases(self, crop: str) -> list:
        """Get common diseases for crop"""
        diseases = {
            'rice': ['Leaf Blight', 'Blast', 'Sheath Blight'],
            'wheat': ['Rust', 'Powdery Mildew', 'Septoria'],
            'cotton': ['Leaf Curl Virus', 'Wilts', 'Blight'],
            'maize': ['Leaf Blight', 'Rust', 'Downy Mildew'],
        }
        return diseases.get(crop.lower(), ['Common fungal diseases'])
    
    def _get_harvest_time(self, crop: str, season: str) -> str:
        """Get harvest time"""
        harvest = {
            ('rice', 'kharif'): 'September-October (120-150 days)',
            ('wheat', 'rabi'): 'March-April (150-180 days)',
            ('maize', 'kharif'): 'August-September (80-120 days)',
            ('cotton', 'kharif'): 'November-December (150-210 days)',
        }
        return harvest.get((crop.lower(), season.lower()), 'Typically 120-180 days')
    
    def _get_expected_yield(self, crop: str) -> str:
        """Get expected yield"""
        yields = {
            'rice': '40-60 quintals/ha',
            'wheat': '40-50 quintals/ha',
            'maize': '30-50 quintals/ha',
            'cotton': '15-20 quintals/ha',
            'groundnut': '15-20 quintals/ha',
        }
        return yields.get(crop.lower(), 'Depends on management')

# Initialize chatbot
farmer_chatbot = FarmerChatbot()
