"""
Fertilizer Recommendation System
Suggests optimal fertilizer based on soil nutrients and crop type
"""

from typing import Dict, List

class FertilizerRecommendation:
    def __init__(self):
        """Initialize fertilizer recommendation system"""
        self.fertilizer_database = {
            'Urea': {
                'nitrogen': 46,
                'phosphorus': 0,
                'potassium': 0,
                'cost_per_kg': 5.5,
                'application_season': ['All'],
                'crops': ['Wheat', 'Rice', 'Maize', 'Sugarcane'],
                'description': 'High nitrogen content, quick release'
            },
            'DAP': {  # Diammonium Phosphate
                'nitrogen': 18,
                'phosphorus': 46,
                'potassium': 0,
                'cost_per_kg': 22,
                'application_season': ['Kharif', 'Rabi'],
                'crops': ['Cotton', 'Groundnut', 'Wheat'],
                'description': 'Balanced N:P ratio, good for seedling'
            },
            'NPK 10-26-26': {
                'nitrogen': 10,
                'phosphorus': 26,
                'potassium': 26,
                'cost_per_kg': 18,
                'application_season': ['All'],
                'crops': ['All'],
                'description': 'Balanced macro nutrients'
            },
            'Muriate of Potash': {
                'nitrogen': 0,
                'phosphorus': 0,
                'potassium': 60,
                'cost_per_kg': 12,
                'application_season': ['All'],
                'crops': ['Sugarcane', 'Banana', 'Potato'],
                'description': 'Pure potassium, improves crop quality'
            },
            'Ammonium Sulfate': {
                'nitrogen': 21,
                'phosphorus': 0,
                'potassium': 0,
                'cost_per_kg': 8,
                'application_season': ['All'],
                'crops': ['Rice', 'Wheat', 'Maize'],
                'description': 'Nitrogen + sulfur, good for acidic soils'
            },
            'Single Super Phosphate': {
                'nitrogen': 0,
                'phosphorus': 16,
                'potassium': 0,
                'cost_per_kg': 10,
                'application_season': ['Kharif', 'Rabi'],
                'crops': ['Legumes', 'Oilseeds'],
                'description': 'Pure phosphorus source'
            },
            'Potassium Nitrate': {
                'nitrogen': 13,
                'phosphorus': 0,
                'potassium': 46,
                'cost_per_kg': 35,
                'application_season': ['Rabi'],
                'crops': ['Vegetables', 'Fruits'],
                'description': 'Premium source for N and K'
            },
            'Bone Meal': {
                'nitrogen': 3,
                'phosphorus': 27,
                'potassium': 0,
                'cost_per_kg': 25,
                'application_season': ['All'],
                'crops': ['Vegetables', 'Fruits', 'Flowers'],
                'description': 'Organic phosphorus source'
            }
        }
        
        self.nutrient_deficiency_symptoms = {
            'Nitrogen': {
                'symptoms': 'Yellowing of lower leaves, stunted growth',
                'fix': 'Apply nitrogen-rich fertilizer',
                'crops_affected': ['Rice', 'Wheat', 'Maize']
            },
            'Phosphorus': {
                'symptoms': 'Purple discoloration, delayed flowering',
                'fix': 'Apply DAP or SSP',
                'crops_affected': ['Cotton', 'Groundnut']
            },
            'Potassium': {
                'symptoms': 'Brown edges on leaves, weak stems',
                'fix': 'Apply potassium-rich fertilizer',
                'crops_affected': ['Sugarcane', 'Banana']
            },
            'Sulfur': {
                'symptoms': 'Yellowing of young leaves',
                'fix': 'Apply ammonium sulfate',
                'crops_affected': ['Oilseeds', 'Legumes']
            },
            'Boron': {
                'symptoms': 'Distorted new growth, poor flowering',
                'fix': 'Apply borax spray',
                'crops_affected': ['Vegetables', 'Fruits']
            }
        }
    
    def analyze_soil(self, nitrogen: float, phosphorus: float, potassium: float, 
                     ph: float, organic_matter: float):
        """
        Analyze soil nutrient levels
        
        Args:
            nitrogen: Soil nitrogen content (kg/ha)
            phosphorus: Soil phosphorus content (kg/ha)
            potassium: Soil potassium content (kg/ha)
            ph: Soil pH
            organic_matter: Organic matter percentage
        
        Returns:
            Analysis dictionary with deficiencies and status
        """
        analysis = {
            'nitrogen_status': '',
            'phosphorus_status': '',
            'potassium_status': '',
            'organic_matter_status': '',
            'ph_status': '',
            'deficiencies': []
        }
        
        # Nitrogen analysis (good: 300-400 kg/ha)
        if nitrogen < 150:
            analysis['nitrogen_status'] = 'Deficient'
            analysis['deficiencies'].append('Nitrogen')
        elif nitrogen < 250:
            analysis['nitrogen_status'] = 'Low'
        elif nitrogen < 500:
            analysis['nitrogen_status'] = 'Medium'
        else:
            analysis['nitrogen_status'] = 'High'
        
        # Phosphorus analysis (good: 20-25 kg/ha)
        if phosphorus < 10:
            analysis['phosphorus_status'] = 'Deficient'
            analysis['deficiencies'].append('Phosphorus')
        elif phosphorus < 15:
            analysis['phosphorus_status'] = 'Low'
        elif phosphorus < 40:
            analysis['phosphorus_status'] = 'Medium'
        else:
            analysis['phosphorus_status'] = 'High'
        
        # Potassium analysis (good: 150-200 kg/ha)
        if potassium < 50:
            analysis['potassium_status'] = 'Deficient'
            analysis['deficiencies'].append('Potassium')
        elif potassium < 100:
            analysis['potassium_status'] = 'Low'
        elif potassium < 300:
            analysis['potassium_status'] = 'Medium'
        else:
            analysis['potassium_status'] = 'High'
        
        # Organic matter (good: 2-3%)
        if organic_matter < 1.5:
            analysis['organic_matter_status'] = 'Low'
            analysis['deficiencies'].append('Organic Matter')
        elif organic_matter < 2.5:
            analysis['organic_matter_status'] = 'Medium'
        else:
            analysis['organic_matter_status'] = 'Good'
        
        # pH analysis (good: 6.0-7.0 for most crops)
        if ph < 5.5:
            analysis['ph_status'] = 'Very Acidic'
        elif ph < 6.0:
            analysis['ph_status'] = 'Acidic'
        elif ph < 8.5:
            analysis['ph_status'] = 'Neutral/Optimal'
        else:
            analysis['ph_status'] = 'Alkaline'
        
        return analysis
    
    def recommend_fertilizer(self, crop: str, soil_analysis: Dict, 
                           season: str, farm_area: float) -> Dict:
        """
        Recommend fertilizers based on crop and soil analysis
        
        Args:
            crop: Crop name
            soil_analysis: Soil analysis dictionary
            season: Current season
            farm_area: Farm area in hectares
        
        Returns:
            Fertilizer recommendations
        """
        recommendations = {
            'primary_fertilizers': [],
            'secondary_applications': [],
            'amendments': [],
            'total_cost_estimate': 0,
            'application_schedule': []
        }
        
        deficiencies = soil_analysis.get('deficiencies', [])
        
        # Primary recommendations based on deficiencies
        for deficiency in deficiencies:
            if deficiency == 'Nitrogen':
                recommendations['primary_fertilizers'].append({
                    'fertilizer': 'Urea',
                    'quantity_kg_per_ha': 100,
                    'total_quantity': 100 * farm_area,
                    'timing': 'Split into 2-3 applications'
                })
            elif deficiency == 'Phosphorus':
                recommendations['primary_fertilizers'].append({
                    'fertilizer': 'DAP',
                    'quantity_kg_per_ha': 50,
                    'total_quantity': 50 * farm_area,
                    'timing': 'Basal application'
                })
            elif deficiency == 'Potassium':
                recommendations['primary_fertilizers'].append({
                    'fertilizer': 'Muriate of Potash',
                    'quantity_kg_per_ha': 40,
                    'total_quantity': 40 * farm_area,
                    'timing': 'Split into 2 applications'
                })
            elif deficiency == 'Organic Matter':
                recommendations['amendments'].append({
                    'amendment': 'Farmyard Manure',
                    'quantity_tons_per_ha': 5,
                    'total_quantity': 5 * farm_area,
                    'timing': 'Before sowing'
                })
        
        # Calculate estimated cost
        for fert in recommendations['primary_fertilizers']:
            cost = fert['total_quantity'] * self.fertilizer_database.get(
                fert['fertilizer'], {}).get('cost_per_kg', 10)
            recommendations['total_cost_estimate'] += cost
        
        # Application schedule
        recommendations['application_schedule'] = [
            '1st Week: Basal application of phosphorus',
            '3rd Week: First nitrogen application',
            '6th Week: Second nitrogen application',
            '9th Week: Potassium application if needed'
        ]
        
        return recommendations
    
    def check_nutrient_deficiency(self, symptoms: str, crop: str) -> Dict:
        """
        Identify nutrient deficiency based on symptoms
        
        Args:
            symptoms: Observed symptoms
            crop: Crop name
        
        Returns:
            Possible deficiencies and recommendations
        """
        deficiencies = []
        
        for nutrient, info in self.nutrient_deficiency_symptoms.items():
            if any(word in symptoms.lower() for word in info['symptoms'].split(',')):
                deficiencies.append({
                    'nutrient': nutrient,
                    'symptoms': info['symptoms'],
                    'recommendation': info['fix'],
                    'severity': 'High' if len(deficiencies) == 0 else 'Medium'
                })
        
        return {
            'identified_deficiencies': deficiencies,
            'crop': crop,
            'immediate_action': deficiencies[0]['recommendation'] if deficiencies else 'Monitor field'
        }
    
    def get_fertilizer_cost_estimate(self, fertilizers: List[Dict]) -> float:
        """Calculate total cost estimate for fertilizers"""
        total_cost = 0
        for fert in fertilizers:
            cost_per_kg = self.fertilizer_database.get(
                fert['name'], {}).get('cost_per_kg', 10)
            total_cost += fert['quantity'] * cost_per_kg
        return total_cost

# Initialize
fertilizer_recommendation = FertilizerRecommendation()
