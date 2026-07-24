#function for importing current weather data for a given location using Open-Meteo API
import requests
from app.models.weather import Weather


class ClimateFetcher:
    # Get latitude and longitude for a given city name using Open-Meteo Geocoding API
    def _get_coordinates(self, city_name):
        params = {
            'name' : city_name,
            'count' : 1
        }
        response = requests.get('https://geocoding-api.open-meteo.com/v1/search', params = params)
        data = response.json()
        lat =  data['results'][0]['latitude']
        lon = data['results'][0]['longitude']
        return lat, lon

    # Fetch current weather data (temperature, humidity, wind speed, UV index) for given coordinates
    def get_weather(self, city_name):
        lat, lon = self._get_coordinates(city_name)
        params = {
        "latitude": lat,
        "longitude": lon,
        "current" : 'temperature_2m,relative_humidity_2m,wind_speed_10m',
        "daily": 'uv_index_max'
        }   
        response = requests.get('https://api.open-meteo.com/v1/forecast', params = params)
        data = response.json()
        temperature = data['current']['temperature_2m']
        humidity = data['current']['relative_humidity_2m']
        wind_speed = data['current']['wind_speed_10m']
        uv = data['daily']['uv_index_max'][0]
        return Weather(
            temperature = temperature,
            humidity = humidity,
            wind_speed = wind_speed,
            uv = uv
            )