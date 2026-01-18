import pandas as pd
from sklearn.preprocessing import LabelEncoder
from sklearn.ensemble import RandomForestRegressor
import joblib

df = pd.read_csv("data/groundwater.csv")

# Clean the dataset
df = df.dropna(subset=["Name of District", "Net Ground Water Availability for future use"])

df = df.rename(columns={
    "Name of District": "District",
    "Net Ground Water Availability for future use": "Net_Groundwater"
})

# Encode district names
le = LabelEncoder()
df["District_Code"] = le.fit_transform(df["District"])

# Features and target
X = df[["District_Code"]]
y = df["Net_Groundwater"]

# Train model
model = RandomForestRegressor()
model.fit(X, y)

# Save model + encoder
joblib.dump(model, "models/water_model.pkl")
joblib.dump(le, "models/water_encoder.pkl")

print("Water forecasting model trained successfully!")
