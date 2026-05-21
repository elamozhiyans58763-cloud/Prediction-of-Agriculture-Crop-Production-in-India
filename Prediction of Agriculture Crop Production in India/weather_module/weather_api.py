"""
Weather API Integration Module
Fetches real-time weather data from OpenWeatherMap API
"""

import requests
import os
from datetime import datetime

class WeatherAPI:
    def __init__(self):
        """Initialize Weather API with API key from environment"""
        self.api_key = os.getenv('OPENWEATHER_API_KEY', 'your_api_key_here')
        self.base_url = 'https://api.openweathermap.org/data/2.5'
        self.forecast_url = 'https://api.openweathermap.org/data/3.0/stations'
    
    def get_current_weather(self, city: str, country_code: str = 'IN'):
        """
        Get current weather for a city
        
        Args:
            city: City name
            country_code: Country code (default: IN for India)
        
        Returns:
            Dictionary with weather data or None if error
        """
        try:
            url = f"{self.base_url}/weather"
            params = {
                'q': f"{city},{country_code}",
                'appid': self.api_key,
                'units': 'metric'
            }
            response = requests.get(url, params=params, timeout=5)
            
            if response.status_code == 200:
                data = response.json()
                return {
                    'city': data['name'],
                    'country': data['sys']['country'],
                    'temperature': data['main']['temp'],
                    'feels_like': data['main']['feels_like'],
                    'humidity': data['main']['humidity'],
                    'pressure': data['main']['pressure'],
                    'weather': data['weather'][0]['main'],
                    'description': data['weather'][0]['description'],
                    'wind_speed': data['wind']['speed'],
                    'wind_degree': data['wind'].get('deg', 0),
                    'clouds': data['clouds']['all'],
                    'rainfall': data.get('rain', {}).get('1h', 0),
                    'visibility': data.get('visibility', 0),
                    'timestamp': datetime.fromtimestamp(data['dt']),
                    'sunrise': datetime.fromtimestamp(data['sys']['sunrise']),
                    'sunset': datetime.fromtimestamp(data['sys']['sunset'])
                }
            else:
                print(f"Error: {response.status_code}")
                return None
        except requests.exceptions.RequestException as e:
            print(f"API Error: {e}")
            return None
    
    def get_weather_forecast(self, city: str, days: int = 5):
        """
        Get weather forecast for next N days
        
        Args:
            city: City name
            days: Number of days to forecast (max 5 for free tier)
        
        Returns:
            List of forecast data
        """
        try:
            url = f"{self.base_url}/forecast"
            params = {
                'q': city,
                'appid': self.api_key,
                'units': 'metric',
                'cnt': min(days * 8, 40)  # API returns data in 3-hour intervals
            }
            response = requests.get(url, params=params, timeout=5)
            
            if response.status_code == 200:
                data = response.json()
                forecasts = []
                
                for item in data['list']:
                    forecasts.append({
                        'timestamp': datetime.fromtimestamp(item['dt']),
                        'temperature': item['main']['temp'],
                        'humidity': item['main']['humidity'],
                        'weather': item['weather'][0]['main'],
                        'rainfall': item.get('rain', {}).get('3h', 0),
                        'wind_speed': item['wind']['speed'],
                        'clouds': item['clouds']['all']
                    })
                
                return forecasts
            else:
                return None
        except requests.exceptions.RequestException as e:
            print(f"API Error: {e}")
            return None
    
    def get_weather_by_coordinates(self, latitude: float, longitude: float):
        """
        Get weather by GPS coordinates
        
        Args:
            latitude: Latitude
            longitude: Longitude
        
        Returns:
            Weather dictionary
        """
        try:
            url = f"{self.base_url}/weather"
            params = {
                'lat': latitude,
                'lon': longitude,
                'appid': self.api_key,
                'units': 'metric'
            }
            response = requests.get(url, params=params, timeout=5)
            
            if response.status_code == 200:
                data = response.json()
                return {
                    'latitude': latitude,
                    'longitude': longitude,
                    'temperature': data['main']['temp'],
                    'humidity': data['main']['humidity'],
                    'weather': data['weather'][0]['main'],
                    'wind_speed': data['wind']['speed'],
                    'rainfall': data.get('rain', {}).get('1h', 0),
                    'timestamp': datetime.fromtimestamp(data['dt'])
                }
            return None
        except requests.exceptions.RequestException as e:
            print(f"API Error: {e}")
            return None
    
    def get_agricultural_recommendations(self, weather_data: Dict) -> Dict:
        """
        Generate agricultural recommendations based on weather
        
        Args:
            weather_data: Current weather data
        
        Returns:
            Recommendations dictionary
        """
        recommendations = {
            'irrigation': '',
            'pesticide_spray': '',
            'harvesting': '',
            'risk_alerts': []
        }
        
        temp = weather_data.get('temperature', 0)
        humidity = weather_data.get('humidity', 0)
        rainfall = weather_data.get('rainfall', 0)
        weather = weather_data.get('weather', '').lower()
        
        # Irrigation recommendations
        if humidity < 40:
            recommendations['irrigation'] = "URGENT: Irrigation needed. Humidity very low."
        elif humidity < 60:
            recommendations['irrigation'] = "Schedule irrigation in next 2-3 days"
        else:
            recommendations['irrigation'] = "Sufficient moisture available. Monitor soil."
        
        # Pesticide spray recommendations
        if humidity > 70 and temp > 20:
            recommendations['pesticide_spray'] = "Ideal conditions for pesticide spray"
            recommendations['risk_alerts'].append("High humidity - watch for fungal diseases")
        elif humidity > 80:
            recommendations['risk_alerts'].append("Very high humidity - high disease risk")
        
        # Temperature based alerts
        if temp < 10:
            recommendations['risk_alerts'].append("Low temperature - protect sensitive crops")
        elif temp > 40:
            recommendations['risk_alerts'].append("High temperature - increase irrigation")
        
        # Weather alerts
        if 'rain' in weather or 'storm' in weather:
            recommendations['risk_alerts'].append("Heavy rainfall expected - monitor fields")
        
        if 'wind' in weather:
            recommendations['risk_alerts'].append("Strong winds reported - check for damage")
        
        return recommendations

# Initialize weather API
weather_api = WeatherAPI()
