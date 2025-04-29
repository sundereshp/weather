from flask import Flask, request, jsonify
import mysql.connector
import requests
from flask_cors import CORS
from datetime import datetime

def format_unix_time(unix_timestamp):
    return datetime.fromtimestamp(unix_timestamp).strftime('%I:%M %p')

app = Flask(__name__)
CORS(app, origins=["http://localhost:8080"])

# Configuration for the database
DB_HOST = "localhost"
DB_USER = "root"
DB_PASSWORD = "Vishal@003"
DB_NAME = "weather_db"

# API Key for OpenWeather
API_KEY = "3dde6c2561d3bd96b2ea0bd48c5ca6bc"

# Function to ensure the database and tables exist
def init_db():
    # Connect to MySQL without specifying a database first
    conn = mysql.connector.connect(
        host=DB_HOST,
        user=DB_USER,
        password=DB_PASSWORD
    )
    cursor = conn.cursor()

    # Create the database if it does not exist
    cursor.execute(f"CREATE DATABASE IF NOT EXISTS {DB_NAME}")
    cursor.execute(f"USE {DB_NAME}")
    
    # Create the current_weather table if it does not exist
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS current_weather (
        id INT AUTO_INCREMENT PRIMARY KEY,
        city_name VARCHAR(255) NOT NULL,
        latitude DOUBLE NOT NULL,
        longitude DOUBLE NOT NULL,
        temperature DOUBLE NOT NULL,
        feels_like DOUBLE NOT NULL,
        humidity DOUBLE NOT NULL,
        pressure DOUBLE NOT NULL,
        wind_speed DOUBLE NOT NULL,
        condition_description VARCHAR(255),
        icon VARCHAR(255),
        visibility DOUBLE,
        sunrise INT NOT NULL,
        sunset INT NOT NULL,
        timestamp INT NOT NULL,
        flag INT DEFAULT 0
    )
    """)
    
    # Create the forecast_weather table if it does not exist
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS forecast_weather (
        id INT AUTO_INCREMENT PRIMARY KEY,
        city_name VARCHAR(255) NOT NULL,
        forecast_date DATETIME NOT NULL,
        temperature DOUBLE NOT NULL,
        condition_description VARCHAR(255),
        icon VARCHAR(255)
    )
    """)
    
    conn.commit()
    cursor.close()
    conn.close()

@app.before_request
def setup():
    init_db()  # Initialize DB and tables when the app starts

@app.route('/search', methods=['GET'])
def search_weather():
    city = request.args.get('city')
    if not city:
        return jsonify({'error': 'City parameter is missing'}), 400

    # Connect to the MySQL database
    conn = mysql.connector.connect(
        host=DB_HOST,
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_NAME
    )
    cursor = conn.cursor(dictionary=True)  # Return rows as dicts

    # Check if the city already exists with flag = 0
    cursor.execute(
        "SELECT * FROM current_weather WHERE city_name = %s AND flag = 0", (city,))
    existing = cursor.fetchone()

    if existing:
        cursor.close()
        conn.close()
        print(f"ℹ️ Using cached weather for {city}")
        return jsonify(existing)

    # If not in DB or flag != 0, fetch from API
    try:
        # Step 1: Get coordinates
        geo_url = f"http://api.openweathermap.org/geo/1.0/direct?q={city}&limit=1&appid={API_KEY}"
        geo_data = requests.get(geo_url).json()
        if not geo_data:
            raise ValueError(f"City '{city}' not found")
        lat, lon = geo_data[0]['lat'], geo_data[0]['lon']

        # Step 2: Current Weather
        weather_url = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={API_KEY}&units=metric"
        weather_data = requests.get(weather_url).json()
        wind_speed_mph = round(weather_data['wind']['speed'] * 2.23694, 2)

        weather_values = (
            lat,
            lon,
            weather_data['main']['temp'],
            weather_data['main']['feels_like'],
            weather_data['main']['humidity'],
            weather_data['main']['pressure'],
            wind_speed_mph,  # ✅ updated to mph
            weather_data['weather'][0]['description'],
            weather_data['weather'][0]['icon'],
            weather_data.get('visibility', 0) / 1000,
            weather_data['sys']['sunrise'],
            weather_data['sys']['sunset'],
            weather_data['dt']
        )

        # Check if city exists
        cursor.execute("SELECT id FROM current_weather WHERE city_name = %s", (city,))
        exists = cursor.fetchone()

        if exists:
            cursor.execute(""" 
                UPDATE current_weather SET
                    latitude = %s,
                    longitude = %s,
                    temperature = %s,
                    feels_like = %s,
                    humidity = %s,
                    pressure = %s,
                    wind_speed = %s,
                    condition_description = %s,
                    icon = %s,
                    visibility = %s,
                    sunrise = %s,
                    sunset = %s,
                    timestamp = %s,
                    flag = 0
                WHERE city_name = %s
            """, weather_values + (city,))
            print(f"🔁 Updated weather for {city}")
        else:
            cursor.execute(""" 
                INSERT INTO current_weather 
                (city_name, latitude, longitude, temperature, feels_like, humidity, pressure, wind_speed, condition_description, icon, visibility, sunrise, sunset, timestamp)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """, (city,) + weather_values)
            print(f"✅ Inserted weather for {city}")

        conn.commit()

        # Step 3: Forecast
        forecast_url = f"https://api.openweathermap.org/data/2.5/forecast?lat={lat}&lon={lon}&appid={API_KEY}&units=metric"
        forecast_data = requests.get(forecast_url).json()

        cursor.execute(
            "DELETE FROM forecast_weather WHERE city_name = %s", (city,))
        for item in forecast_data['list']:
            forecast_time = item['dt_txt']
            temp = item['main']['temp']
            description = item['weather'][0]['description']
            icon = item['weather'][0]['icon']

            cursor.execute(""" 
                INSERT INTO forecast_weather
                (city_name, forecast_date, temperature, condition_description, icon)
                VALUES (%s, %s, %s, %s, %s)
            """, (city, forecast_time, temp, description, icon))
        conn.commit()
        print(f"📅 Forecast for {city} updated")

        response_data = {
            'city_name': city,
            'temperature': weather_data['main']['temp'],
            'condition_description': weather_data['weather'][0]['description'],
            'feels_like': weather_data['main']['feels_like'],
            'humidity': weather_data['main']['humidity'],
            'pressure': weather_data['main']['pressure'],
            # convert to km
            'visibility': weather_data.get('visibility', 0) / 1000,
            # static for now (OpenWeather OneCall API needed for live UV)
            'uvIndex': 3,
            'sunrise': format_unix_time(weather_data['sys']['sunrise']),
            'sunset': format_unix_time(weather_data['sys']['sunset'])
        }

        cursor.close()
        conn.close()
        return jsonify(response_data)

    except Exception as e:
        cursor.close()
        conn.close()
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    init_db()  # Ensure the database and tables are created when the app starts
    app.run(debug=True, host='0.0.0.0', port=5000)
