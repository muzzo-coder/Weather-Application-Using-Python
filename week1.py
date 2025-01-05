import requests
import tkinter as tk
from tkinter import messagebox
import sqlite3
from datetime import datetime

# Database setup for storing operation history
def setup_database():
    conn = sqlite3.connect('weather_history.db')
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS history (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        location TEXT,
                        temperature TEXT,
                        humidity TEXT,
                        wind_speed TEXT,
                        timestamp TEXT
                    )''')
    conn.commit()
    conn.close()

# Function to save operation history
def save_to_database(location, temperature, humidity, wind_speed):
    conn = sqlite3.connect('weather_history.db')
    cursor = conn.cursor()
    cursor.execute('''INSERT INTO history (location, temperature, humidity, wind_speed, timestamp)
                      VALUES (?, ?, ?, ?, ?)''',
                   (location, temperature, humidity, wind_speed, datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
    conn.commit()
    conn.close()

# Function to fetch weather data from OpenWeatherMap API
def get_weather_data(location):
    api_key = '641536db3ec8eba03adaaa4ce5f8075e'
    base_url = 'https://api.openweathermap.org/data/2.5/weather'

    params = {
        'q': location,
        'appid': api_key,
        'units': 'metric'  # Fetch data in Celsius
    }

    response = requests.get(base_url, params=params)

    if response.status_code == 200:
        data = response.json()
        weather_info = {
            'temperature': data['main']['temp'],
            'humidity': data['main']['humidity'],
            'wind_speed': data['wind']['speed']
        }
        return weather_info
    else:
        return None

# Function to display weather data in the GUI
def display_weather():
    location = location_entry.get()
    if not location:
        messagebox.showerror("Error", "Please enter a location.")
        return

    weather_data = get_weather_data(location)
    if weather_data:
        temperature_label.config(text=f"Temperature: {weather_data['temperature']} \u00b0C")
        humidity_label.config(text=f"Humidity: {weather_data['humidity']}%")
        wind_speed_label.config(text=f"Wind Speed: {weather_data['wind_speed']} m/s")
        save_to_database(location, weather_data['temperature'], weather_data['humidity'], weather_data['wind_speed'])
    else:
        messagebox.showerror("Error", "Could not fetch weather data. Check the location or API key.")

# Tkinter GUI setup
setup_database()
root = tk.Tk()
root.title("Weather Application")
root.geometry("400x300")

# Input field
location_label = tk.Label(root, text="Enter Location:")
location_label.pack(pady=10)

location_entry = tk.Entry(root, width=30)
location_entry.pack(pady=5)

# Fetch weather button
fetch_button = tk.Button(root, text="Get Weather", command=display_weather)
fetch_button.pack(pady=10)

# Weather information labels
temperature_label = tk.Label(root, text="Temperature: ", font=("Arial", 12))
temperature_label.pack(pady=5)

humidity_label = tk.Label(root, text="Humidity: ", font=("Arial", 12))
humidity_label.pack(pady=5)

wind_speed_label = tk.Label(root, text="Wind Speed: ", font=("Arial", 12))
wind_speed_label.pack(pady=5)

root.mainloop()
