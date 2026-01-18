# smart-rural-ai-system
The Smart Rural AI System is an integrated AI-powered platform designed to support farmers and rural communities with intelligent, data-driven agricultural solutions. It combines Machine Learning, Deep Learning, NLP, and real-world datasets to offer actionable insights and automate essential rural services.

📌 Overview

The Smart Rural AI System is an integrated AI-powered platform designed to support farmers and rural communities with crop recommendation, pest detection, water forecasting, market prediction, chatbots, and grievance management.

This project uses Machine Learning, Deep Learning, NLP, and real datasets to deliver actionable insights to farmers, improve decision-making, and strengthen governance.

🚀 Features
✔ 1. Crop Recommendation System

Recommends the most suitable crop using environmental and soil parameters.
Uses ML algorithms & real agricultural datasets.

✔ 2. Pest Detection Using CNN

Farmers upload an image → CNN model detects pest category.
Trained on Kaggle Agricultural Pest Dataset.

✔ 3. Water Availability Forecasting

Predicts Net Ground Water Availability for each district.
Uses government groundwater resources dataset.

✔ 4. Market / Yield Prediction

Predicts crop yield using NPK, temperature, humidity, pH, rainfall, and crop name.

✔ 5. Farmer Chatbot (Telugu + English)

AI chatbot assists with:

Crop season suggestions

Fertilizer recommendations

Pest & disease information

Government scheme details

Insurance, PMFBY, Rythu Bharosa

✔ 6. AI Grievance Management System

Automatically:
✔ Classifies complaint → Department
✔ Detects duplicates
✔ Assigns priority levels
✔ Generates ticket ID
✔ Tracks complaint status

✔ 7. Secure Login + Beautiful UI (Flask + Streamlit)

Signup & Login system (Flask)

Green-themed animated UI (Streamlit)

Home dashboard with feature cards

🧠 Tech Stack
Languages & Tools

Python

Streamlit

Flask

NumPy, Pandas

Scikit-learn

TensorFlow/Keras

SQLite

Machine Learning Models

Random Forest (Crop Recommendation)

Regression Models (Yield & Water Forecasting)

CNN (Pest Detection)

NLP-based Classification (Grievance System)

📂 Project Structure
Smart_Rural_AI_System/
│
├── app.py (Flask - Login routing)
├── streamlit_app.py (Main AI dashboard)
├── requirements.txt
│
├── models/
│   ├── crop_model.pkl
│   ├── soil_encoder.pkl
│   ├── crop_encoder.pkl
│   ├── water_model.pkl
│   ├── water_encoder.pkl
│   ├── market_model.pkl
│   ├── pest_model.h5
│   └── pest_labels.pkl
│
├── data/
│   ├── crop_data.csv
│   ├── pest_dataset/
│   ├── groundwater_data.csv
│   ├── market_prices.csv
│   └── grievances.csv
│
├── utils/
│   ├── chatbot.py
│   ├── grievance_ai.py
│   ├── train_models.py
│   ├── train_pest_model.py
│   └── train_water_model.py
│
├── templates/ (Flask UI)
│   ├── signup.html
│   ├── login.html
│   └── home.html
│
└── static/
    └── css, images, icons

🛠 Setup Instructions
1️⃣ Clone the Repository
git clone https://github.com/your-username/smart-rural-ai-system.git
cd smart-rural-ai-system

2️⃣ Install Dependencies
pip install -r requirements.txt

3️⃣ Run Flask (Signup/Login + Home Dashboard)
python app.py


Access login page:
➡ http://127.0.0.1:5000/

4️⃣ Run Streamlit (AI Features)
streamlit run streamlit_app.py

5️⃣ Click Feature Cards in Home Page

Flask redirects to Streamlit modules like:

http://localhost:8501/?page=crop
http://localhost:8501/?page=pest
http://localhost:8501/?page=water
