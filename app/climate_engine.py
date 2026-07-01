#function for importing current weather data for a given location using Open-Meteo API
import requests

def coordinates(city_name):
    params = {
        'name' : city_name,
        'count' : 1
    }
    response = requests.get('https://geocoding-api.open-meteo.com/v1/search', params = params)
    data = response.json()
    lat =  data['results'][0]['latitude']
    lon = data['results'][0]['longitude']
    return lat, lon

def weather_data(lat,lon):
    params = {
    "latitude": lat,
    "longitude": lon,
    "current" : 'temperature_2m,relative_humidity_2m'
    }   
    response = requests.get('https://api.open-meteo.com/v1/forecast', params = params)
    data = response.json()
    temp = data['current']['temperature_2m']
    humidity = data['current']['relative_humidity_2m']
    return temp, humidity
