import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
import joblib

# ---------------- LOAD DATA ----------------
crop = pd.read_csv("data/crop_data.csv")

print("Original columns:")
print(crop.columns)

# ---------------- RENAME COLUMNS (FIX SPELLING) ----------------
crop = crop.rename(columns={
    "Temparature": "Temperature",
    "Phosphorous": "Phosphorus"
})

print("Renamed columns:")
print(crop.columns)

# ---------------- ENCODE CATEGORICAL DATA ----------------
soil_encoder = LabelEncoder()
crop["Soil Type"] = soil_encoder.fit_transform(crop["Soil Type"])

crop_encoder = LabelEncoder()
crop["Crop Type"] = crop_encoder.fit_transform(crop["Crop Type"])

# ---------------- FEATURES & TARGET ----------------
X = crop[
    [
        "Temperature",
        "Humidity",
        "Moisture",
        "Soil Type",
        "Nitrogen",
        "Potassium",
        "Phosphorus"
    ]
]

y = crop["Crop Type"]

# ---------------- TRAIN MODEL ----------------
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X, y)

# ---------------- SAVE MODELS ----------------
joblib.dump(model, "models/crop_model.pkl")
joblib.dump(crop_encoder, "models/crop_encoder.pkl")
joblib.dump(soil_encoder, "models/soil_encoder.pkl")

print("✅ Crop recommendation model trained successfully")
