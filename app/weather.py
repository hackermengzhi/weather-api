import httpx
import os
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("OPENWEATHER_API_KEY")

BASE_URL = "https://api.openweathermap.org/data/2.5/weather"


async def get_coordinates(client, city):
    response = await client.get("http://api.openweathermap.org/geo/1.0/direct", params={
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
        response = await client.get(BASE_URL, params={
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