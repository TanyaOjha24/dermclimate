from app.acquisition.climate_fetcher import ClimateFetcher
from app.persistence.snowflake_connector import save_climate_log, save_ingredient_scan, save_user_session
from app.risk.tewl_risk_engine import TEWLRiskEngine
from app.features.feature_engineer import engineer_features

climate_fetcher  = ClimateFetcher()
weather = climate_fetcher .get_weather("Boston")
engine = TEWLRiskEngine()
features = engineer_features(weather)
risk = engine.score(features)

save_climate_log('Boston', weather.temperature, weather.humidity, weather.wind_speed, weather.uv, risk.score)

print(f"Temperature: {weather.temperature}°C")
print(f"Humidity: {weather.humidity}%")
print(f"Wind Speed: {weather.wind_speed} km/h")
print(f"UV Index: {weather.uv}")
print(f"Barrier Risk Score: {risk.score}/100")

from app.acquisition.ingredient_fetcher import IngredientFetcher

ingredient_fetcher = IngredientFetcher()

ingredients = ingredient_fetcher.get_product_ingredients(
    "CeraVe Moisturizing Cream"
)
save_ingredient_scan('Cerave Moisturizing Cream', ingredients)

save_user_session('Boston', 'Cerave', 'dry skin', risk.score)