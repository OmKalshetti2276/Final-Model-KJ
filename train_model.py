import pandas as pd
import joblib
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor

data = pd.read_csv("realistic_dataset.csv")

X = data.drop(columns=["soil_moisture_after"])
y = data["soil_moisture_after"]

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

model = RandomForestRegressor(n_estimators=200, max_depth=15)
model.fit(X_train, y_train)

joblib.dump(model, "soil_response_model.pkl")
print("Model trained.")
