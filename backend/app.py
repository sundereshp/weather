from flask import Flask, request, jsonify
import mysql.connector
import requests
from flask_cors import CORS
from datetime import datetime
import time

app = Flask(__name__)
CORS(app, origins=["http://localhost:8080"])

# Configuration for the database
DB_HOST = "localhost"
DB_USER = "root"
DB_PASSWORD = "Vishal@003"
DB_NAME = "weather_db"

# API Key for OpenWeather
API_KEY = "3dde6c2561d3bd96b2ea0bd48c5ca6bc"

def format_unix_time(unix_timestamp):
    return datetime.fromtimestamp(unix_timestamp).strftime('%I:%M %p')

def init_db():
    conn = mysql.connector.connect(
        host=DB_HOST,
        user=DB_USER,
        password=DB_PASSWORD
    )
    cursor = conn.cursor()
    cursor.execute(f"CREATE DATABASE IF NOT EXISTS {DB_NAME}")
    cursor.execute(f"USE {DB_NAME}")

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS current_weather (
            id INT AUTO_INCREMENT PRIMARY KEY,
            city_name VARCHAR(255) NOT NULL,
            latitude DECIMAL(10,8) NOT NULL,
            longitude DECIMAL(11,8) NOT NULL,
            temperature DECIMAL(5,1) NOT NULL,
            condition_description VARCHAR(255) NOT NULL,
            feels_like DECIMAL(5,1) NOT NULL,
            humidity DECIMAL(5,2) NOT NULL,
            pressure DECIMAL(6,2) NOT NULL,
            wind_speed DECIMAL(5,2) NOT NULL,
            visibility DECIMAL(6,2) NOT NULL,
            sunrise BIGINT NOT NULL,
            sunset BIGINT NOT NULL,
            timestamp BIGINT NOT NULL,
            flag TINYINT DEFAULT 0,
            UNIQUE (city_name)
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS forecast_weather (
            id INT AUTO_INCREMENT PRIMARY KEY,
            city_name VARCHAR(255) NOT NULL,
            forecast_date VARCHAR(255) NOT NULL,
            temperature DECIMAL(5,1) NOT NULL,
            condition_description VARCHAR(255) NOT NULL,
            icon VARCHAR(255),
            FOREIGN KEY (city_name) REFERENCES current_weather(city_name)
        )
    """)

    conn.commit()
    cursor.close()
    conn.close()
    print(f"✅ Database and tables initialized")

@app.before_request
def setup():
    init_db()

@app.route('/search', methods=['GET'])
def search_weather():
    city = request.args.get('city')
    if not city:
        return jsonify({'error': 'City parameter is missing'}), 400

    try:
        print(f"🔍 Searching for weather data for {city}")
        geo_url = f"http://api.openweathermap.org/geo/1.0/direct?q={city}&limit=1&appid={API_KEY}"
        geo_response = requests.get(geo_url)
        geo_data = geo_response.json()
        if not geo_data:
            return jsonify({'error': f"City '{city}' not found"}), 404
        lat, lon = geo_data[0]['lat'], geo_data[0]['lon']

        weather_url = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={API_KEY}&units=metric"
        weather_response = requests.get(weather_url)
        weather_data = weather_response.json()
        if weather_data.get('cod') != 200:
            return jsonify({'error': weather_data.get('message', 'Failed to fetch weather data')}), 500

        wind_speed_mph = round(weather_data['wind']['speed'] * 2.23694, 2)

        forecast_data = None
        forecast_list = []

        try:
            forecast_url = f"https://api.openweathermap.org/data/2.5/forecast?lat={lat}&lon={lon}&appid={API_KEY}&units=metric"
            forecast_response = requests.get(forecast_url)
            forecast_data = forecast_response.json()
            if forecast_data.get('cod') != "200":
                forecast_data = None
        except Exception as e:
            print(f"⚠️ Forecast API Error: {str(e)}")
            forecast_data = None

        if forecast_data:
            daily = {}
            for item in forecast_data['list']:
                date_str = item['dt_txt']
                day = datetime.fromisoformat(date_str).strftime('%a')
                temp = item['main']['temp']
                description = item['weather'][0]['description']
                icon = item['weather'][0]['icon']

                if day not in daily:
                    daily[day] = {
                        'day': day,
                        'high': temp,
                        'low': temp,
                        'condition': description,
                        'precipitation': 0,
                        'icon': icon
                    }
                else:
                    daily[day]['high'] = max(daily[day]['high'], temp)
                    daily[day]['low'] = min(daily[day]['low'], temp)

            forecast_list = list(daily.values())

        current_weather = {
            'city_name': city,
            'temperature': weather_data['main']['temp'],
            'condition_description': weather_data['weather'][0]['description'],
            'feels_like': weather_data['main']['feels_like'],
            'humidity': weather_data['main']['humidity'],
            'pressure': weather_data['main']['pressure'],
            'wind_speed': wind_speed_mph,
            'visibility': weather_data.get('visibility', 0) / 1000,
            'uvIndex': 3,
            'sunrise': format_unix_time(weather_data['sys']['sunrise']),
            'sunset': format_unix_time(weather_data['sys']['sunset']),
            'forecast': forecast_list[:5] if forecast_list else []
        }

        db_weather = {
            'city_name': city,
            'latitude': lat,
            'longitude': lon,
            'temperature': weather_data['main']['temp'],
            'condition_description': weather_data['weather'][0]['description'],
            'feels_like': weather_data['main']['feels_like'],
            'humidity': weather_data['main']['humidity'],
            'pressure': weather_data['main']['pressure'],
            'wind_speed': wind_speed_mph,
            'visibility': weather_data.get('visibility', 0) / 1000,
            'sunrise': weather_data['sys']['sunrise'],
            'sunset': weather_data['sys']['sunset'],
            'timestamp': int(time.time())
        }

        conn = mysql.connector.connect(
            host=DB_HOST,
            user=DB_USER,
            password=DB_PASSWORD,
            database=DB_NAME
        )
        cursor = conn.cursor(dictionary=True)

        cursor.execute("SELECT id FROM current_weather WHERE city_name = %s", (city,))
        exists = cursor.fetchone()

        if exists:
            cursor.execute(""" 
                UPDATE current_weather SET
                    latitude = %s,
                    longitude = %s,
                    temperature = %s,
                    condition_description = %s,
                    feels_like = %s,
                    humidity = %s,
                    pressure = %s,
                    wind_speed = %s,
                    visibility = %s,
                    sunrise = %s,
                    sunset = %s,
                    timestamp = %s,
                    flag = 0
                WHERE city_name = %s
            """, (
                db_weather['latitude'],
                db_weather['longitude'],
                db_weather['temperature'],
                db_weather['condition_description'],
                db_weather['feels_like'],
                db_weather['humidity'],
                db_weather['pressure'],
                db_weather['wind_speed'],
                db_weather['visibility'],
                db_weather['sunrise'],
                db_weather['sunset'],
                db_weather['timestamp'],
                city
            ))
        else:
            cursor.execute(""" 
                INSERT INTO current_weather 
                (city_name, latitude, longitude, temperature, condition_description, feels_like, humidity, pressure, wind_speed, visibility, sunrise, sunset, timestamp)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """, (
                city,
                db_weather['latitude'],
                db_weather['longitude'],
                db_weather['temperature'],
                db_weather['condition_description'],
                db_weather['feels_like'],
                db_weather['humidity'],
                db_weather['pressure'],
                db_weather['wind_speed'],
                db_weather['visibility'],
                db_weather['sunrise'],
                db_weather['sunset'],
                db_weather['timestamp']
            ))

        if forecast_data:
            cursor.execute("DELETE FROM forecast_weather WHERE city_name = %s", (city,))
            for item in forecast_data['list']:
                forecast_time = item['dt_txt']
                temp = item['main']['temp']
                description = item['weather'][0]['description']
                icon = item['weather'][0]['icon']
                cursor.execute("""
                    INSERT INTO forecast_weather 
                    (city_name, forecast_date, temperature, condition_description, icon)
                    VALUES (%s, %s, %s, %s, %s)
                """, (
                    city, forecast_time, temp, description, icon
                ))

        conn.commit()
        cursor.close()
        conn.close()

        return jsonify(current_weather)

    except Exception as e:
        import traceback
        print(f"❌ Error: {str(e)}\n{traceback.format_exc()}")
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    init_db()
    app.run(debug=True, host='0.0.0.0', port=5000)
