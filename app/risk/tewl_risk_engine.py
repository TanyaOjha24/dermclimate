from app.risk.risk_engine import RiskEngine

class TEWLRiskEngine (RiskEngine):
    def score(self, features):
        # Calculate skin barrier risk score (0-100) based on climate variables using TEWL clinical thresholds
        temp = features["temperature"]
        humidity = features["humidity"]
        wind_speed = features["wind_speed"]
        uv = features["uv"]

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
    
    def version(self):
        return 'tewl-v1'
        