# ===================== IMPORTS =====================
import streamlit as st
import joblib
import numpy as np
from PIL import Image
import tensorflow as tf

# Backend modules (KEEP THEM)
from utils.chatbot import chatbot_response
from utils.grievance_ai import process_grievance, track_complaint

# ===================== GLOBAL CUSTOM CSS =====================
st.markdown("""
    <style>

    /* Background Image */
    body {
        background-image: url('https://img.freepik.com/free-photo/farm-landscape_1417-1635.jpg');
        background-size: cover;
        background-attachment: fixed;
        background-repeat: no-repeat;
        opacity: 0.98;
    }

    /* Main container background blur */
    .main {
        background: rgba(255, 255, 255, 0.85);
        padding: 25px;
        border-radius: 12px;
    }

    /* Title Styling */
    h1, h2, h3 {
        font-family: 'Poppins', sans-serif;
        font-weight: 700;
        color: #145A32;
    }

    /* Sub Headers */
    .stSubheader, h4 {
        color: #1B5E20;
        font-weight: 600;
    }

    /* Beautiful Buttons */
    .stButton>button {
        background-color: #27ae60;
        color: white;
        border-radius: 10px;
        padding: 10px 25px;
        font-size: 16px;
        border: none;
        transition: 0.3s;
    }
    .stButton>button:hover {
        background-color: #1e8449;
        transform: scale(1.04);
    }

    /* Text Inputs */
    .stTextInput>div>div>input {
        border: 2px solid #27ae60;
        border-radius: 8px;
        padding: 8px;
    }

    /* Sliders */
    .stSlider>div>div>div {
        background-color: #27ae60 !important;
    }

    /* File Upload Box */
    .uploadedFile {
        border: 2px dashed #27ae60;
        border-radius: 12px;
        background-color: rgba(255, 255, 255, 0.8);
    }

    /* Feature Box */
    .feature-card {
        background: white;
        padding: 20px;
        border-radius: 15px;
        box-shadow: 0px 4px 12px rgba(0,0,0,0.15);
        transition: 0.3s;
        margin-bottom: 25px;
    }
    .feature-card:hover {
        transform: scale(1.02);
        box-shadow: 0px 6px 16px rgba(0,0,0,0.25);
    }

    </style>
""", unsafe_allow_html=True)

# ===================== PAGE CONFIG =====================
st.set_page_config(page_title="Smart Rural AI System", layout="wide")

# ===================== URL BASED ROUTING =====================

query_params = st.query_params
page = query_params.get("page", "home")

 # default: home


# ===================== LOAD MODELS =====================
crop_model = joblib.load("models/crop_model.pkl")
crop_encoder = joblib.load("models/crop_encoder.pkl")
soil_encoder = joblib.load("models/soil_encoder.pkl")

water_model = joblib.load("models/water_model.pkl")
water_encoder = joblib.load("models/water_encoder.pkl")

market_model = joblib.load("models/market_model.pkl")

pest_model = tf.keras.models.load_model("models/pest_model.h5")
pest_classes = [
    'ants', 'bees', 'beetle', 'catterpillar',
    'earthworms', 'earwig', 'grasshopper',
    'moth', 'slug', 'snail', 'wasp', 'weevil'
]


# ===================== FEATURE UI FUNCTIONS =====================

# ---------- HOME UI ----------
def home_ui():
    st.title("🌱 Smart Rural AI System")
    st.write("Welcome! Please open features from the Flask Home Page.")
    st.info("This Streamlit app loads one module at a time based on URL parameters.")
    

# ---------- CROP RECOMMENDATION ----------
def crop_ui():
    st.markdown("<div class='feature-card'>", unsafe_allow_html=True)
    st.header("🌾 Crop Recommendation")

    temperature = st.slider("🌡 Temperature (°C)", 10, 45, 25)
    humidity = st.slider("💧 Humidity (%)", 20, 100, 60)
    moisture = st.slider("🌱 Soil Moisture (%)", 0, 100, 50)

    soil_type = st.selectbox("🧪 Soil Type", soil_encoder.classes_)
    soil_encoded = soil_encoder.transform([soil_type])[0]

    nitrogen = st.slider("🔬 Nitrogen (N)", 0, 150, 20)
    potassium = st.slider("🟢 Potassium (K)", 0, 150, 10)
    phosphorus = st.slider("🟡 Phosphorus (P)", 0, 150, 10)

    if st.button("Predict Best Crop"):
        features = [[temperature, humidity, moisture,
                     soil_encoded, nitrogen, potassium, phosphorus]]

        pred = crop_model.predict(features)
        crop_name = crop_encoder.inverse_transform(pred)[0]

        st.success(f"🌱 **Recommended Crop: {crop_name}**")

    st.markdown("</div>", unsafe_allow_html=True)


# ---------- CHATBOT ----------
def chatbot_ui():
    st.markdown("<div class='feature-card'>", unsafe_allow_html=True)
    st.header("🤖 Farmer Chatbot (Telugu + English)")

    query = st.text_input("Ask your question:")

    if query:
        response = chatbot_response(query)
        st.info(response)

    st.markdown("</div>", unsafe_allow_html=True)



# ---------- GRIEVANCE SYSTEM ----------
def grievance_ui():
    st.markdown("<div class='feature-card'>", unsafe_allow_html=True)
    st.header("🏛 AI-Powered Grievance Management")

    complaint = st.text_area("Describe your issue")

    if st.button("Submit Complaint"):
        out = process_grievance(complaint)

        st.success(f"🏷 Department: {out['department']}")
        st.warning(f"⚡ Priority: {out['priority']}")
        st.info(f"🎫 Ticket ID: {out['ticket']}")

        if out["duplicate"]:
            st.error("⚠ Duplicate complaint detected!")

        st.write(out["forward"])

    st.subheader("🔍 Track Complaint")
    ticket = st.text_input("Enter Ticket ID")

    if st.button("Track Status"):
        st.info(track_complaint(ticket))

    st.markdown("</div>", unsafe_allow_html=True)



# ---------- WATER FORECAST ----------
def water_ui():
    st.markdown("<div class='feature-card'>", unsafe_allow_html=True)
    st.header("💧 Water Availability Prediction")

    district = st.text_input("🏡 Enter District Name")

    if st.button("Predict Water Level"):
        try:
            code = water_encoder.transform([district])[0]
            prediction = water_model.predict([[code]])[0]
            st.success(f"💧 Net Ground Water Availability: **{prediction:.2f} units**")
        except:
            st.error("District not found. Please check spelling.")

    st.markdown("</div>", unsafe_allow_html=True)


# ---------- MARKET PREDICTION ----------
def market_ui():
    st.markdown("<div class='feature-card'>", unsafe_allow_html=True)
    st.header("📈 Crop Yield Prediction")

    N = st.number_input("Nitrogen (N)")
    P = st.number_input("Phosphorus (P)")
    K = st.number_input("Potassium (K)")
    temp = st.number_input("Temperature")
    hum = st.number_input("Humidity")
    ph = st.number_input("pH Value")
    rain = st.number_input("Rainfall")
    crop = st.text_input("Crop Name")

    if st.button("Predict Yield"):
        try:
            c = crop_encoder.transform([crop])[0]
            features = [[N,P,K,temp,hum,ph,rain,c]]
            pred = market_model.predict(features)[0]
            st.success(f"🌾 Estimated Yield: **{pred:.2f} kg/acre**")
        except:
            st.error("Unknown crop. Check spelling.")

    st.markdown("</div>", unsafe_allow_html=True)



# ---------- PEST DETECTION ----------
def pest_ui():
    st.markdown("<div class='feature-card'>", unsafe_allow_html=True)
    st.header("🐛 Pest Detection System")

    uploaded_file = st.file_uploader("📤 Upload Pest Image", type=["jpg", "jpeg", "png"])

    if uploaded_file:
        img = Image.open(uploaded_file).convert("RGB")
        img = img.resize((150,150))

        st.image(img, caption="Uploaded Image", width=250)

        img_arr = np.array(img)/255.0
        img_arr = img_arr.reshape(1,150,150,3)

        prediction = pest_model.predict(img_arr)
        idx = np.argmax(prediction)
        confidence = np.max(prediction)*100

        pest_name = pest_classes[idx]

        st.success(f"🪲 Detected Pest: **{pest_name}**")
        st.info(f"📊 Confidence: {confidence:.2f}%")

    st.markdown("</div>", unsafe_allow_html=True)



# ===================== ROUTING LOGIC =====================
if page == "crop":
    crop_ui()

elif page == "chatbot":
    chatbot_ui()

elif page == "grievance":
    grievance_ui()

elif page == "water":
    water_ui()

elif page == "market":
    market_ui()

elif page == "pest":
    pest_ui()

else:
    home_ui()
