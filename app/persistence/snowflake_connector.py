import snowflake.connector
from app.config import (
    SNOWFLAKE_USER,
    SNOWFLAKE_PASSWORD,
    SNOWFLAKE_ACCOUNT,
    SNOWFLAKE_DATABASE,
    SNOWFLAKE_SCHEMA,
    SNOWFLAKE_WAREHOUSE,
)

def get_snowflake_connection():

    conn = snowflake.connector.connect(
    account=SNOWFLAKE_ACCOUNT,
    user=SNOWFLAKE_USER,
    password=SNOWFLAKE_PASSWORD,
    database=SNOWFLAKE_DATABASE,
    schema=SNOWFLAKE_SCHEMA,
    warehouse=SNOWFLAKE_WAREHOUSE
    )
    return conn

'''conn = get_snowflake_connection()
print("Connected successfully!")
conn.close()'''

def setup_database():
    conn = get_snowflake_connection()
    cursor = conn.cursor() 
    cursor.execute("CREATE DATABASE IF NOT EXISTS DERMCLIMATE")
    cursor.execute("USE DATABASE DERMCLIMATE")       
    cursor.execute (""" 
        CREATE TABLE if not exists climate_logs (
            city VARCHAR,
            timestamp TIMESTAMP,
            temperature FLOAT,
            humidity FLOAT,
            wind_speed FLOAT,
            uv_index FLOAT,
            barrier_risk_score FLOAT
        )  
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS ingredient_scans (
            product_name VARCHAR,
            ingredient_list VARCHAR,
            timestamp TIMESTAMP
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS user_sessions (
            city_searched VARCHAR,
            product_scanned VARCHAR,
            timestamp TIMESTAMP,
            skin_type VARCHAR,
            barrier_risk_score FLOAT
        )
    """)
    cursor.execute("ALTER TABLE climate_logs ADD COLUMN IF NOT EXISTS session_id VARCHAR")
    cursor.execute("ALTER TABLE ingredient_scans ADD COLUMN IF NOT EXISTS session_id VARCHAR")
    cursor.execute("ALTER TABLE user_sessions ADD COLUMN IF NOT EXISTS session_id VARCHAR")
    cursor.close()
    conn.close()               

'''test = setup_database()
print("setup successful")'''

def save_climate_log(city, temp, humidity, wind_speed, uv, risk_score):
    conn = get_snowflake_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO climate_logs(city, timestamp, temperature, humidity, wind_speed, uv_index, barrier_risk_score)
        VALUES (%s, current_timestamp, %s, %s, %s, %s, %s)
    """, (city, temp, humidity, wind_speed, uv, risk_score))
    cursor.close()
    conn.close()

def save_ingredient_scan(product_name, ingredient_list): 
    conn = get_snowflake_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO ingredient_scans(product_name, ingredient_list, timestamp)
        VALUES (%s, %s, current_timestamp)
    """, (product_name, ingredient_list))
    cursor.close()
    conn.close()

def save_user_session(city_searched, product_scanned, skin_type, risk_score):
    conn = get_snowflake_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO user_sessions(city_searched, product_scanned, timestamp, skin_type, barrier_risk_score)
        VALUES (%s, %s, current_timestamp, %s, %s)
    """, (city_searched, product_scanned, skin_type, risk_score))
    cursor.close()
    conn.close()

