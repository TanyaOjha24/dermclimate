from app.climate_engine import coordinates, weather_data, calculate_barrier_risk
from app.snowflake_connector import save_climate_log, save_ingredient_scan, save_user_session

lat, lon = coordinates('Boston')
temp, humidity, wind_speed, uv = weather_data(lat, lon)
risk = calculate_barrier_risk(temp, humidity, wind_speed, uv)
save_climate_log('Boston', temp, humidity, wind_speed, uv, risk)


print(f"Temperature: {temp}°C")
print(f"Humidity: {humidity}%")
print(f"Wind Speed: {wind_speed} km/h")
print(f"UV Index: {uv}")
print(f"Barrier Risk Score: {risk}/100")

from app.ingredient_engine import get_product_ingredients

ingredients = get_product_ingredients('CeraVe Moisturizing Cream')
print(ingredients)
save_ingredient_scan('Cerave Moisturizing Cream', ingredients)

save_user_session('Boston', 'Cerave', 'dry skin', risk)