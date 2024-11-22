import openmeteo_requests
import requests_cache
import pandas as pd
from retry_requests import retry
from openmeteo_sdk.Variable import Variable


class WeatherDataProcessor:
    def __init__(self):
        # init weather lib with session, reuses same connection
        cache_session = requests_cache.CachedSession('.weather_cache', expire_after=3600)
        retry_session = retry(cache_session, retries=5, backoff_factor=0.2)
        self.openmeteo = openmeteo_requests.Client(session=retry_session)
    
    def fetch_weather_data(self, latitude, longitude):
        url = "https://api.open-meteo.com/v1/forecast"
        params = {
            "latitude": latitude,
            "longitude": longitude,
            "current": ["temperature_2m", "weather_code"],
            "hourly": "weather_code",
        }
        
        def celsius_to_fahrenheit(celsius):
                fahrenheit = (celsius * 9/5) + 32
                return fahrenheit

        # get API response from open meteo
        try:
            responses = self.openmeteo.weather_api("https://api.open-meteo.com/v1/forecast", params=params)
            response = responses[0]
            current = response.Current()

            current_variables = list(map(lambda i: current.Variables(i), 
                range(0, current.VariablesLength())))
            current_temperature_2m = next(filter(lambda x: x.Variable() 
                == Variable.temperature and x.Altitude() == 2, current_variables))

            curr_temp = celsius_to_fahrenheit(current_temperature_2m.Value())      
            weather_code = response.Hourly().Variables(1)
            
            # Extract weather conditions
            return {
                "current_weather": {
                    "temperature": int(curr_temp),
                    "current_code": weather_code
                }
            }
        
        except Exception as e:
            print(f"error {str(e)}")
            return {}
    
    # convert raw data for weather reccomender model
    def process_weather_data(self, weather_data):
        # error handling
        if not weather_data or 'current_weather' not in weather_data:
            return {
                "temperature_category": "None",
                "condition": "None"
            }
        
        # Extract current weather information
        temperature = weather_data['current_weather'].get('temperature', 0)
        weathercode = weather_data['current_weather'].get('current_code', 0)
        print(weathercode)
        # Categorize temperature
        temperature_category = self._categorize_temperature(temperature)
        
        # Map weathercode to condition
        condition = self._map_weathercode_to_condition(weathercode)
        
        return {
            "temperature_category": temperature_category,
            "condition": condition,
            "raw_temperature": temperature,
            "raw_weathercode": weathercode
        }
    
     # categorize the temp by degrees 
    def _categorize_temperature(self, temperature):
       
        if temperature < 40:
            return "cold"
        elif 40 <= temperature < 60:
            return "mild"
        elif 60 <= temperature < 80:
            return "warm"
        elif temperature >= 80:
            return "hot"
        else:
            return "unknown"
    
    # find out condition and return string 
    def _map_weathercode_to_condition(self, weathercode):
        clear_codes = [0, 1]
        partly_cloudy_codes = [2, 3]
        cloudy_codes = [45, 48]
        rain_codes = [51, 53, 55, 61, 63, 65, 80, 81, 82]
        snow_codes = [71, 73, 75, 85, 86]

        if weathercode in clear_codes:
            return "sunny"
        elif weathercode in cloudy_codes or weathercode in partly_cloudy_codes:
            return "cloudy"
        elif weathercode in rain_codes:
            return "rainy"
        elif weathercode in snow_codes:
            return "snowy"
        else:
            return "windy"
        
# Usage example
def get_weather_recommendation(latitude, longitude):
    processor = WeatherDataProcessor()
    
    # Fetch weather data
    weather_data = processor.fetch_weather_data(latitude, longitude)
   
    # Process weather data
    processed_weather = processor.process_weather_data(weather_data)
    
    return processed_weather
