from dataclasses import dataclass

@dataclass
class EngineeredWeather:
    temperature : float
    humidity: float
    wind_speed: float
    uv: float
    humid_category : str
    temp_category : str
    uv_category : str
    wind_category : str