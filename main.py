# Fetch current weather data for a given location using Open-Meteo API
import requests

params = {
    "latitude": 42.36,
    "longitude": -71.06,
    "current" : 'temperature_2m,relative_humidity_2m'
}
response = requests.get("https://api.open-meteo.com/v1/forecast", params = params)
data = response.json()
#print(data)

temp = data['current']['temperature_2m']
humidity = data['current']['relative_humidity_2m']

print(f'temperature ={temp}\n humidity = {humidity}')