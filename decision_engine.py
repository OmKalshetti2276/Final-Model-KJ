import joblib
import pandas as pd

MODEL_PATH = "soil_response_model.pkl"
STRESS_THRESHOLD = 35
IRRIGATION_OPTIONS = [0, 5, 10, 15, 20, 30]

model = joblib.load(MODEL_PATH)

def predict_soil_moisture(
    temperature, humidity, wind_speed, et_15min,
    rain_mm, rain_intensity, soil_moisture,
    irrigation_seconds, crop="maize",
    soil_type_factor=1.0, slope_factor=1.0, growth_stage_factor=1.0
):
    X = pd.DataFrame([{
        "temperature": temperature,
        "humidity": humidity,
        "wind_speed": wind_speed,
        "et_15min": et_15min,
        "rain_mm": rain_mm,
        "rain_intensity": rain_intensity,
        "soil_moisture_before": soil_moisture,
        "irrigation_seconds": irrigation_seconds,
        "soil_type_factor": soil_type_factor,
        "slope_factor": slope_factor,
        "growth_stage_factor": growth_stage_factor
    }])

    crop_cols = [c for c in model.feature_names_in_ if c.startswith("crop_")]
    for col in crop_cols:
        X[col] = 1 if col == f"crop_{crop}" else 0

    return float(model.predict(X)[0])

def decide_irrigation(
    temperature, humidity, wind_speed, et_15min,
    rain_mm, rain_intensity, current_sm, crop="maize",
    soil_type_factor=1.0, slope_factor=1.0, growth_stage_factor=1.0
):

    predicted_no_irrigation = predict_soil_moisture(
        temperature, humidity, wind_speed, et_15min,
        rain_mm, rain_intensity, current_sm,
        0, crop, soil_type_factor, slope_factor, growth_stage_factor
    )

    if predicted_no_irrigation >= STRESS_THRESHOLD:
        return {"action": "WAIT", "irrigation_seconds": 0, "predicted_sm": round(predicted_no_irrigation, 2)}

    for sec in IRRIGATION_OPTIONS[1:]:
        predicted_sm = predict_soil_moisture(
            temperature, humidity, wind_speed, et_15min,
            rain_mm, rain_intensity, current_sm,
            sec, crop, soil_type_factor, slope_factor, growth_stage_factor
        )
        if predicted_sm >= STRESS_THRESHOLD:
            return {"action": "IRRIGATE", "irrigation_seconds": sec, "predicted_sm": round(predicted_sm, 2)}


# This is our fallback mechanism in case if no duration in our list
# satisfies the condition to take up our moisture to above threshold
    return {"action": "IRRIGATE", "irrigation_seconds": IRRIGATION_OPTIONS[-1], "predicted_sm": round(predicted_sm, 2)}
