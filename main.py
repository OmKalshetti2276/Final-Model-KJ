import json
from fastapi import FastAPI
from pydantic import BaseModel
from datetime import datetime
from decision_engine import decide_irrigation
from fao56 import calculate_eto
from crop_water import calculate_etc



app = FastAPI(title="Irrigation AI Engine")

history_data=[]



# class FarmProfile(BaseModel):
    

class WeatherInput(BaseModel):
    temperature: float
    humidity: float
    wind_speed: float
    solar_radiation: float
    rain_mm: float
    rain_intensity: int = 1
    soil_moisture: float
    crop: str ="generic"
    soil_type: str
    slope: str
    growth_stage: str
    # land_size: float

soil_map = {"sandy": 0.8, "loam": 1.0, "clay": 1.2}
slope_map = {"flat": 1.0, "mild": 0.9, "steep": 0.8}
stage_map = {"early": 0.7, "mid": 1.2, "late": 1.0}

# @app.post("/setup")
# def setup_farm(profile: FarmProfile):
#     with open(PROFILE_FILE, "w") as f:
#         json.dump(profile.dict(), f)
#     return {"status": "Profile saved"}

@app.get("/")
def home():
    return {"status": "Irrigation ML API Running"}


@app.post("/predict")
def predict(data: WeatherInput):
    # with open(PROFILE_FILE) as f:
    #     profile = json.load(f)

    soil_factor = soil_map.get(data.soil_type, 1.0)
    slope_factor = slope_map.get(data.slope, 1.0)
    stage_factor = stage_map.get(data.growth_stage, 1.0)

    eto_daily = calculate_eto(data.temperature, data.humidity, data.wind_speed, 0.0864*data.solar_radiation)
    etc_daily = calculate_etc(eto_daily, data.crop)
    et_15min = etc_daily / 96

    result= decide_irrigation(
        temperature=data.temperature,
        humidity=data.humidity,
        wind_speed=data.wind_speed,
        et_15min=et_15min,
        rain_mm=data.rain_mm,
        rain_intensity=data.rain_intensity,
        current_sm=data.soil_moisture,
        crop=data.crop,
        soil_type_factor=soil_factor,
        slope_factor=slope_factor,
        growth_stage_factor=stage_factor
    )

     # Save record for charts
    record = {
        "timestamp": datetime.now().isoformat(),
        "soilMoisture": result["predicted_sm"],
        "et0": data.et_15min * 96,  # approx daily ET
        "temp": data.temperature,
        "humidity": data.humidity,
        "wind": data.wind_speed,
        "solar": 400,  # placeholder
    }

    history_data.append(record)


    # keep last 100 points
    if len(history_data) > 100:
        history_data.pop(0)

    return result

@app.get("/data")
def get_history():
    return history_data

