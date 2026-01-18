import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import LabelEncoder
import joblib

df = pd.read_csv("data/market_prices.csv")

df = df.dropna()

# Encode crop name
le = LabelEncoder()
df["Crop_Code"] = le.fit_transform(df["Crop"])

X = df[[
    "Nitrogen","Phosphorus","Potassium",
    "Temperature","Humidity","pH_Value",
    "Rainfall","Crop_Code"
]]

y = df["Yield"]

model = RandomForestRegressor()
model.fit(X, y)

joblib.dump(model, "models/market_model.pkl")
joblib.dump(le, "models/crop_encoder.pkl")

print("Market/Yield model trained successfully!")
