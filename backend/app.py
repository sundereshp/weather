from flask import Flask, request, jsonify
from flask_cors import CORS
import sqlite3
from datetime import datetime

app = Flask(__name__)
CORS(app, origins=["http://localhost:8080", "http://localhost:3000"])

# Database configuration
DATABASE = 'weather.db'

# Initialize database
def init_db():
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    
    # Create weather table if not exists
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS weather (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            city TEXT NOT NULL,
            temperature REAL,
            condition TEXT,
            high REAL,
            low REAL,
            humidity INTEGER,
            wind REAL,
            feels_like REAL,
            visibility REAL,
            pressure INTEGER,
            uv_index INTEGER,
            sunrise TEXT,
            sunset TEXT,
            last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    conn.commit()
    conn.close()

# Initialize database when app starts
init_db()

@app.route("/api/weather", methods=["GET"])
def get_weather():
    city = request.args.get("city")
    
    if not city:
        return jsonify({"error": "City name is required"}), 400
    
    try:
        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()
        
        # Get the latest weather data for the city
        cursor.execute('''
            SELECT * FROM weather 
            WHERE city = ? 
            ORDER BY last_updated DESC 
            LIMIT 1
        ''', (city,))
        
        result = cursor.fetchone()
        
        if result:
            # Convert the result to a dictionary
            weather_data = {
                "city": result[1],
                "temperature": result[2],
                "condition": result[3],
                "high": result[4],
                "low": result[5],
                "humidity": result[6],
                "wind": result[7],
                "feels_like": result[8],
                "visibility": result[9],
                "pressure": result[10],
                "uv_index": result[11],
                "sunrise": result[12],
                "sunset": result[13],
                "last_updated": result[14]
            }
            return jsonify(weather_data)
        else:
            return jsonify({"error": "No weather data found for this city"}), 404
            
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        conn.close()

@app.route("/api/weather", methods=["POST"])
def update_weather():
    try:
        data = request.json
        city = data.get("city")
        
        if not city:
            return jsonify({"error": "City name is required"}), 400
            
        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()
        
        # Insert or update weather data
        cursor.execute('''
            INSERT INTO weather (
                city, temperature, condition, high, low, humidity, wind, 
                feels_like, visibility, pressure, uv_index, sunrise, sunset
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            city,
            data.get("temperature"),
            data.get("condition"),
            data.get("high"),
            data.get("low"),
            data.get("humidity"),
            data.get("wind"),
            data.get("feels_like"),
            data.get("visibility"),
            data.get("pressure"),
            data.get("uv_index"),
            data.get("sunrise"),
            data.get("sunset")
        ))
        
        conn.commit()
        return jsonify({"message": "Weather data updated successfully"})
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        conn.close()

if __name__ == "__main__":
    app.run(debug=True, port=5000)