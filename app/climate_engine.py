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
    "current" : 'temperature_2m,relative_humidity_2m,wind_speed_10m',
    "daily": 'uv_index_max'
    }   
    response = requests.get('https://api.open-meteo.com/v1/forecast', params = params)
    data = response.json()
    temp = data['current']['temperature_2m']
    humidity = data['current']['relative_humidity_2m']
    wind_speed = data['current']['wind_speed_10m']
    uv = data['daily']['uv_index_max'][0]
    return temp, humidity, wind_speed, uv


def calculate_barrier_risk(temp, humidity, wind_speed, uv):
    ideal_temp = (18, 22)
    ideal_humidity = (40, 60)
    ideal_uv = (0, 2)
    ideal_wind = (0, 10)

    if temp < ideal_temp[0]:
        temp_deviation = ideal_temp[0] - temp
    elif temp > ideal_temp[1]:
        temp_deviation = temp - ideal_temp[1]
    else:
        temp_deviation = 0
    
    if humidity < ideal_humidity[0]:
        humidity_deviation = ideal_humidity[0] - humidity
    elif humidity > ideal_humidity[1]:
        humidity_deviation = humidity - ideal_humidity[1]
    else:
        humidity_deviation = 0

    if uv < ideal_uv[0]:
        uv_deviation = ideal_uv[0] - uv
    elif uv > ideal_uv[1]:
        uv_deviation = uv - ideal_uv[1]
    else:
        uv_deviation = 0

    if wind_speed < ideal_wind[0]:
        wind_deviation = ideal_wind[0] - wind_speed
    elif wind_speed > ideal_wind[1]:
        wind_deviation = wind_speed - ideal_wind[1]
    else:
        wind_deviation = 0      
    
    temp_score = temp_deviation / 30
    humidity_score = humidity_deviation / 20
    uv_score = uv_deviation / 9
    wind_score = wind_deviation / 90

    total = (humidity_score * 40) + (uv_score * 40) + (temp_score * 15) + (wind_score * 5)
    total = round(min(total, 100), 1)
    return total