import numpy as np
import pandas as pd
from fao56 import calculate_eto
from crop_water import calculate_etc

N = 5000
data = []

soil_map = {"sandy": 0.8, "loam": 1.0, "clay": 1.2}
slope_map = {"flat": 1.0, "mild": 0.9, "steep": 0.8}
stage_map = {"early": 0.7, "mid": 1.2, "late": 1.0}

for _ in range(N):
    temperature = np.random.uniform(18, 38)
    humidity = np.random.uniform(30, 85)
    wind_speed = np.random.uniform(0.5, 6)
    solar_radiation = np.random.uniform(12, 28)

    rain_mm = np.random.uniform(0, 8)
    rain_intensity = np.random.choice([0, 1, 2])

    soil_moisture_before = np.random.uniform(20, 60)

    soil_type = np.random.choice(list(soil_map.keys()))
    slope = np.random.choice(list(slope_map.keys()))
    stage = np.random.choice(list(stage_map.keys()))

    soil_factor = soil_map[soil_type]
    slope_factor = slope_map[slope]
    stage_factor = stage_map[stage]

    eto_daily = calculate_eto(temperature, humidity, wind_speed, solar_radiation)
    etc_daily = calculate_etc(eto_daily, "maize")
    et_15min = etc_daily / 96

    irrigation_seconds = np.random.choice([0, 5, 10, 15, 20, 30])

    a, b = 10, 0.09
    irrigation_gain = soil_factor * slope_factor * stage_factor * a * (1 - np.exp(-b * irrigation_seconds))

    rain_gain = rain_mm * 0.25 * (rain_intensity + 1)

    soil_moisture_after = soil_moisture_before - et_15min + irrigation_gain + rain_gain
    soil_moisture_after = min(85, max(10, soil_moisture_after))

    data.append([
        temperature, humidity, wind_speed, et_15min,
        rain_mm, rain_intensity, soil_moisture_before,
        irrigation_seconds, soil_moisture_after,
        soil_factor, slope_factor, stage_factor
    ])

columns = [
    "temperature", "humidity", "wind_speed", "et_15min",
    "rain_mm", "rain_intensity", "soil_moisture_before",
    "irrigation_seconds", "soil_moisture_after",
    "soil_type_factor", "slope_factor", "growth_stage_factor"
]

pd.DataFrame(data, columns=columns).to_csv("realistic_dataset.csv", index=False)
print("Dataset created.")
