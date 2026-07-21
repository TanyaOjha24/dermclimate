def engineer_features(weather):
    
    temp = weather["temperature"]
    humidity = weather["humidity"]
    wind_speed = weather["wind_speed"]
    uv = weather["uv"]

# calculate humidity category
    if 40 <= humidity <= 60:
        humid_category = "optimal"
    elif 20 <= humidity < 40 :
        humid_category = "dry"
    elif humidity < 20:
        humid_category = "critically_dry"
    elif  60 <= humidity < 80 :
        humid_category = "humid"
    else:
        humid_category = "high_humid"

#calculate temp category
    if 18 <= temp <= 22:
        temp_category = "optimal"
    elif temp < 10:
        temp_category = "cold"
    elif 10 <= temp < 18:
        temp_category = "cool"
    elif 22 < temp <= 31:
        temp_category = "warm"
    else:
        temp_category = "hot"

#calculate uv category (WHO scale)
    if uv <= 2:
        uv_category = "low"
    elif 2 < uv <=5:
        uv_category = "moderate"
    elif 5 <= uv < 7:
        uv_category = "high"
    elif 7 <= uv < 10:
        uv_category = "very high"
    else:
        uv_category = "extreme"

#calculate wind categories
    if wind_speed < 10:
        wind_category = "calm"
    elif 11 <= wind_speed < 20:
        wind_category = "light"
    elif 20 <= wind_speed < 40:
        wind_category = "moderate"
    else:
        wind_category = "strong"

    return {
        "temperature": temp,
        "humidity": humidity,
        "wind_speed": wind_speed,
        "uv": uv,
        "humid_category" : humid_category,
        "temp_category" : temp_category,
        "uv_category" : uv_category,
        "wind_category" : wind_category
    }