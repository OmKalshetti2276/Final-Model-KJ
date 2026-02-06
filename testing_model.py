from decision_engine import decide_irrigation
from fao56 import calculate_eto
from crop_water import calculate_etc

# ---------- FARM PROFILE (Simulating farmer input) ----------
crop = "maize"
soil_type_factor = 1.2      # clay
slope_factor = 0.9          # mild slope
growth_stage_factor = 1.2   # mid stage


# ---------- WEATHER DATA (Simulated API data) ----------
temperature = 45
humidity = 55
wind_speed = 3.2
solar_radiation = 22
rain_mm = 44
rain_intensity = 2
soil_moisture = 32


# ---------- STEP 1: FAO56 ET0 ----------
eto_daily = calculate_eto(temperature, humidity, wind_speed, solar_radiation)

# ---------- STEP 2: Crop ET ----------
etc_daily = calculate_etc(eto_daily, crop)

# ---------- STEP 3: Convert to 15-minute ET ----------
et_15min = etc_daily / 96


# ---------- STEP 4: AI Decision ----------
result = decide_irrigation(
    temperature=temperature,
    humidity=humidity,
    wind_speed=wind_speed,
    et_15min=et_15min,
    rain_mm=rain_mm,
    rain_intensity=rain_intensity,
    current_sm=soil_moisture,
    crop=crop,
    soil_type_factor=soil_type_factor,
    slope_factor=slope_factor,
    growth_stage_factor=growth_stage_factor
)

print("", result)
