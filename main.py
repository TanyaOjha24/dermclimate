from app.climate_engine import coordinates, weather_data, calculate_barrier_risk

lat, lon = coordinates('Boston')
temp, humidity, wind_speed, uv = weather_data(lat, lon)
risk = calculate_barrier_risk(temp, humidity, wind_speed, uv)

print(f"Temperature: {temp}°C")
print(f"Humidity: {humidity}%")
print(f"Wind Speed: {wind_speed} km/h")
print(f"UV Index: {uv}")
print(f"Barrier Risk Score: {risk}/100")