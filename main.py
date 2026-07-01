from app.climate_engine import coordinates, weather_data

lat, lon = coordinates('Boston')
print(weather_data(lat, lon))
