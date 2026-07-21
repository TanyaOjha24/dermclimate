from app.acquisition.climate_fetcher import coordinates, weather_data
from app.persistence.snowflake_connector import save_climate_log, save_ingredient_scan, save_user_session
from app.risk.tewl_risk_engine import TEWLRiskEngine

lat, lon = coordinates('Boston')
weather = weather_data(lat, lon)
engine = TEWLRiskEngine()
risk = engine.score(weather)

save_climate_log('Boston', weather["temperature"], weather["humidity"], weather["wind_speed"], weather["uv"], risk)

print(f"Temperature: {weather['temperature']}°C")
print(f"Humidity: {weather['humidity']}%")
print(f"Wind Speed: {weather['wind_speed']} km/h")
print(f"UV Index: {weather['uv']}")
print(f"Barrier Risk Score: {risk}/100")

from app.acquisition.ingredient_fetcher import get_product_ingredients

ingredients = get_product_ingredients('CeraVe Moisturizing Cream')
print(ingredients)
save_ingredient_scan('Cerave Moisturizing Cream', ingredients)

save_user_session('Boston', 'Cerave', 'dry skin', risk)