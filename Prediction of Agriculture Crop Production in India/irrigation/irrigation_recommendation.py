"""
Smart Irrigation Recommendation System
Predicts irrigation needs based on weather, soil moisture, and crop requirements
"""

from datetime import datetime, timedelta
from typing import Dict, List

class IrrigationRecommendation:
    def __init__(self):
        """Initialize irrigation recommendation system"""
        self.crop_water_requirements = {
            'Rice': {'total_mm': 1000, 'peak_demand': 8, 'season': 'Kharif'},
            'Wheat': {'total_mm': 450, 'peak_demand': 5, 'season': 'Rabi'},
            'Maize': {'total_mm': 500, 'peak_demand': 6, 'season': 'Kharif'},
            'Sugarcane': {'total_mm': 1500, 'peak_demand': 8, 'season': 'All'},
            'Cotton': {'total_mm': 650, 'peak_demand': 6, 'season': 'Kharif'},
            'Groundnut': {'total_mm': 400, 'peak_demand': 4, 'season': 'Kharif'},
            'Soybean': {'total_mm': 450, 'peak_demand': 5, 'season': 'Kharif'},
            'Tomato': {'total_mm': 400, 'peak_demand': 3, 'season': 'All'},
            'Potato': {'total_mm': 400, 'peak_demand': 4, 'season': 'Rabi'},
            'Onion': {'total_mm': 450, 'peak_demand': 3, 'season': 'Rabi'}
        }
        
        self.soil_water_capacity = {
            'Sandy': {'field_capacity': 15, 'wilting_point': 5, 'available_water': 10},
            'Loamy': {'field_capacity': 25, 'wilting_point': 10, 'available_water': 15},
            'Clay': {'field_capacity': 35, 'wilting_point': 15, 'available_water': 20}
        }
    
    def calculate_water_requirement(self, crop: str, growth_stage: int, 
                                   rainfall: float):
        """
        Calculate water requirement for a crop
        
        Args:
            crop: Crop name
            growth_stage: Days since sowing (1-150)
            rainfall: Total rainfall received (mm)
        
        Returns:
            Water requirement analysis
        """
        if crop not in self.crop_water_requirements:
            return {'error': 'Crop not found in database'}
        
        crop_info = self.crop_water_requirements[crop]
        total_water_needed = crop_info['total_mm']
        
        # Estimate water needed based on growth stage
        stage_percentage = min((growth_stage / 150) * 100, 100)
        cumulative_water_needed = (total_water_needed * stage_percentage) / 100
        
        # Calculate irrigation requirement
        remaining_water = cumulative_water_needed - rainfall
        irrigation_needed = max(0, remaining_water)
        
        return {
            'crop': crop,
            'growth_stage': growth_stage,
            'days_since_sowing': growth_stage,
            'total_water_requirement': total_water_needed,
            'cumulative_water_needed': cumulative_water_needed,
            'rainfall_received': rainfall,
            'irrigation_required': irrigation_needed,
            'peak_demand_period': 'Days 50-100' if growth_stage < 100 else 'Days 100-150',
            'unit': 'mm'
        }
    
    def calculate_soil_moisture(self, soil_type: str, water_depth: float):
        """
        Calculate soil moisture status
        
        Args:
            soil_type: Type of soil
            water_depth: Water retained in soil (mm)
        
        Returns:
            Soil moisture analysis
        """
        if soil_type not in self.soil_water_capacity:
            soil_type = 'Loamy'  # Default
        
        capacity = self.soil_water_capacity[soil_type]
        field_capacity = capacity['field_capacity']
        wilting_point = capacity['wilting_point']
        available_water = capacity['available_water']
        
        # Calculate moisture percentage
        moisture_percentage = (water_depth / field_capacity) * 100
        
        # Determine status
        if water_depth >= field_capacity:
            status = 'Saturated'
            action = 'Do not irrigate - allow soil to drain'
        elif water_depth >= (available_water * 0.75):
            status = 'Optimal'
            action = 'No irrigation needed'
        elif water_depth >= (available_water * 0.5):
            status = 'Good'
            action = 'Plan irrigation soon'
        elif water_depth >= wilting_point:
            status = 'Low'
            action = 'Irrigate immediately'
        else:
            status = 'Critical'
            action = 'Emergency irrigation required'
        
        return {
            'soil_type': soil_type,
            'current_water_depth_mm': water_depth,
            'field_capacity_mm': field_capacity,
            'wilting_point_mm': wilting_point,
            'available_water_mm': available_water,
            'moisture_percentage': moisture_percentage,
            'moisture_status': status,
            'recommended_action': action
        }
    
    def generate_irrigation_schedule(self, crop: str, soil_type: str, 
                                    start_date: str, season: str) -> List[Dict]:
        """
        Generate irrigation schedule for the season
        
        Args:
            crop: Crop name
            soil_type: Soil type
            start_date: Sowing date (YYYY-MM-DD format)
            season: Season (Kharif/Rabi)
        
        Returns:
            List of irrigation events with dates and quantities
        """
        if crop not in self.crop_water_requirements:
            return [{'error': 'Crop not in database'}]
        
        crop_info = self.crop_water_requirements[crop]
        total_water = crop_info['total_mm']
        
        # Parse start date
        try:
            start = datetime.strptime(start_date, '%Y-%m-%d')
        except:
            start = datetime.now()
        
        schedule = []
        
        # Create irrigation events (typically 4-6 times per season)
        num_irrigations = 5
        days_between_irrigation = 150 // num_irrigations
        water_per_irrigation = total_water / num_irrigations
        
        for i in range(num_irrigations):
            irrigation_date = start + timedelta(days=days_between_irrigation * (i + 1))
            
            schedule.append({
                'event_number': i + 1,
                'date': irrigation_date.strftime('%Y-%m-%d'),
                'days_after_sowing': days_between_irrigation * (i + 1),
                'water_required_mm': water_per_irrigation,
                'water_required_liters_per_ha': water_per_irrigation * 10000,
                'stage': self._get_crop_stage(days_between_irrigation * (i + 1)),
                'priority': 'High' if i in [1, 2] else 'Medium'
            })
        
        return schedule
    
    def _get_crop_stage(self, days: int) -> str:
        """Determine crop growth stage from days since sowing"""
        if days < 30:
            return 'Germination and establishment'
        elif days < 60:
            return 'Vegetative growth'
        elif days < 90:
            return 'Flowering'
        elif days < 120:
            return 'Fruit/Grain development'
        else:
            return 'Maturation'
    
    def calculate_irrigation_efficiency(self, water_applied: float, 
                                       water_used_by_crop: float) -> Dict:
        """
        Calculate irrigation efficiency and water use efficiency
        
        Args:
            water_applied: Total water applied (mm)
            water_used_by_crop: Water actually used by crop (mm)
        
        Returns:
            Efficiency metrics
        """
        efficiency = (water_used_by_crop / water_applied) * 100 if water_applied > 0 else 0
        water_loss = water_applied - water_used_by_crop
        
        return {
            'water_applied_mm': water_applied,
            'water_used_by_crop_mm': water_used_by_crop,
            'water_loss_mm': water_loss,
            'irrigation_efficiency_percentage': efficiency,
            'efficiency_rating': self._rate_efficiency(efficiency),
            'recommendations': self._get_efficiency_recommendations(efficiency)
        }
    
    def _rate_efficiency(self, efficiency: float) -> str:
        """Rate irrigation efficiency"""
        if efficiency > 90:
            return 'Excellent'
        elif efficiency > 80:
            return 'Good'
        elif efficiency > 70:
            return 'Fair'
        elif efficiency > 60:
            return 'Poor'
        else:
            return 'Very Poor'
    
    def _get_efficiency_recommendations(self, efficiency: float) -> List[str]:
        """Get recommendations based on efficiency"""
        recommendations = []
        
        if efficiency < 70:
            recommendations.append('Consider drip irrigation to reduce water loss')
            recommendations.append('Fix any leaks in irrigation system')
            recommendations.append('Improve water management practices')
        
        if efficiency < 80:
            recommendations.append('Schedule irrigation based on soil moisture')
            recommendations.append('Avoid over-irrigation')
        
        if efficiency < 60:
            recommendations.append('Urgent: Review irrigation system')
            recommendations.append('Consider system upgrade or maintenance')
        
        if efficiency > 85:
            recommendations.append('Excellent water management - maintain current practices')
        
        return recommendations
    
    def predict_water_stress(self, soil_moisture: float, temperature: float, 
                           humidity: float, wind_speed: float) -> Dict:
        """
        Predict water stress conditions
        
        Args:
            soil_moisture: Soil moisture percentage (0-100)
            temperature: Air temperature (°C)
            humidity: Relative humidity (%)
            wind_speed: Wind speed (km/h)
        
        Returns:
            Water stress prediction
        """
        # Calculate evapotranspiration estimate (simplified)
        et_rate = (temperature * 0.2) + (wind_speed * 0.1) - (humidity * 0.15)
        et_rate = max(0, et_rate)
        
        # Calculate stress index
        stress_index = (100 - soil_moisture) * (et_rate / 10)
        
        if stress_index < 20:
            stress_level = 'No stress'
            action = 'Monitor soil moisture'
        elif stress_index < 40:
            stress_level = 'Mild stress'
            action = 'Prepare for irrigation'
        elif stress_index < 60:
            stress_level = 'Moderate stress'
            action = 'Irrigate within 2-3 days'
        elif stress_index < 80:
            stress_level = 'High stress'
            action = 'Irrigate within 1-2 days'
        else:
            stress_level = 'Severe stress'
            action = 'Irrigate immediately'
        
        return {
            'soil_moisture_percentage': soil_moisture,
            'temperature': temperature,
            'humidity': humidity,
            'wind_speed': wind_speed,
            'estimated_et_rate_mm_per_day': et_rate,
            'water_stress_index': stress_index,
            'stress_level': stress_level,
            'recommended_action': action,
            'urgency': 'Critical' if stress_index > 70 else 'Normal'
        }

# Initialize
irrigation_recommendation = IrrigationRecommendation()
