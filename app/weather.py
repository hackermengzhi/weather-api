import httpx
import os
from dotenv import load_dotenv

load_dotenv()
# API_KEY = os.getenv("OPENWEATHER_API_KEY")
API_KEY= "75b20b4644770f5eb51c2231c3cc7dbc"
BASE_URL = "https://api.openweathermap.org"
async def get_coordinates(client, city):
    response = await client.get(BASE_URL+ "/geo/1.0/direct", params={
        "q": city,
        "limit": 1,
        "appid": API_KEY
    })
    response.raise_for_status()
    data = response.json()
    if not data:
        raise ValueError(f"City not found: {city}")
    return data[0]["lat"], data[0]["lon"], data[0]["name"], data[0]["country"]

async def get_weather(city: str) -> dict:
    async with httpx.AsyncClient() as client:
        lat, lon, resolved_name, country = await get_coordinates(client, city)
        response = await client.get(BASE_URL+"/data/2.5/weather", params={
            "lat": lat,
            "lon": lon,
            "appid": API_KEY,
            "units": "metric"
        })
        response.raise_for_status()
        data = response.json()
        return {
            "city": resolved_name,
            "country": country,
            "temperature_c": data["main"]["temp"],
            "feels_like_c": data["main"]["feels_like"],
            "description": data["weather"][0]["description"],
            "humidity_percent": data["main"]["humidity"]
        }

async def get_forcast_weather(city) -> dict:
    async with httpx.AsyncClient() as client:
        lat, lon, resolved_name, country = await get_coordinates(client, city)
        response = await client.get(BASE_URL+ "/data/2.5/forecast", params={
            "lat": lat,
            "lon": lon,
            "appid": API_KEY,
            "cnt": 5
        })
        response.raise_for_status()
        data = response.json()
        forecast = []
        for item in data["list"]:
            forecast.append({
                "datetime": item["dt_txt"],
                "temperature_c": item["main"]["temp"],
                "feels_like_c": item["main"]["feels_like"],
                "description": item["weather"][0]["description"],
                "humidity_percent": item["main"]["humidity"],
                "rain_probability": item.get("pop", 0)  # probability of precipitation
            })
        return {
            "city": resolved_name,
            "country": country,
            "forecast": forecast
        }