from fastapi import FastAPI, HTTPException, Query
from app.weather import get_weather

app = FastAPI(title="Weather API", version="1.0")

@app.get("/")
def root():
    return {"message": "Weather API is running"}
@app.get("/weather")
async def weather_by_city(city: str = Query(..., description="City name, e.g. Auckland")):
    try:
        return await get_weather(city)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Weather service error")
