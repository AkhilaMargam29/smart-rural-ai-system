import os
import re
import pdfplumber

# -----------------------------------------------------------
# LOAD GOVERNMENT PDF KNOWLEDGE BASE (RAG)
# -----------------------------------------------------------

def load_pdf_knowledge():
    text = ""
    folder = "rag_docs"
    if not os.path.exists(folder):
        return ""

    for file in os.listdir(folder):
        if file.endswith(".pdf"):
            try:
                with pdfplumber.open(os.path.join(folder, file)) as pdf:
                    for page in pdf.pages:
                        content = page.extract_text()
                        if content:
                            text += content.lower() + "\n"
            except:
                pass
    return text

pdf_data = load_pdf_knowledge()


def rag_answer(query):
    """Return sentences from government PDFs if relevant."""
    if not pdf_data:
        return None

    query = query.lower()
    sentences = pdf_data.split(".")
    results = [s.strip() for s in sentences if query in s]

    return results[:3] if results else None


# -----------------------------------------------------------
# ALL CROPS KNOWLEDGE BASE
# -----------------------------------------------------------

crop_info = {
    "paddy": "Paddy grows best in rainy season (June–September). Requires standing water.",
    "rice": "Rice (Paddy) prefers high rainfall, puddled fields.",
    "cotton": "Cotton grows well in Kharif season. Needs moderate rainfall.",
    "maize": "Maize grows in both Kharif & Rabi. Good in medium rainfall.",
    "wheat": "Wheat is a Rabi crop. Grows in winter.",
    "chilli": "Chilli requires warm climate, moderate irrigation.",
    "groundnut": "Groundnut thrives in sandy loam soil & moderate rainfall.",
    "sugarcane": "Sugarcane grows year-round but prefers high water availability.",
    "turmeric": "Turmeric grows well in rainy season & loamy soil.",
    "millets": "Millets grow best in drylands with less rain.",
    "bajra": "Bajra (Pearl Millet) is drought-resistant.",
    "jowar": "Jowar grows in dry areas with low rainfall.",
    "soybean": "Soybean is ideal for Kharif season.",
}


# -----------------------------------------------------------
# SEASON-BASED CROPS
# -----------------------------------------------------------

seasonal_crops = {
    "rainy": ["Paddy", "Cotton", "Maize", "Turmeric", "Soybean", "Groundnut"],
    "kharif": ["Paddy", "Cotton", "Maize", "Soybean", "Turmeric"],
    "summer": ["Vegetables", "Millets", "Sunflower"],
    "winter": ["Wheat", "Mustard", "Barley"],
}


# -----------------------------------------------------------
# FERTILIZER DATABASE (REAL ADVICE)
# -----------------------------------------------------------

fertilizer_advice = {
    "paddy": "Basal: DAP + MOP + FYM; Tillering: Urea; Panicle initiation: Light Urea.",
    "cotton": "Basal: DAP + Potash; 35 days: Urea; Flowering: Potash.",
    "maize": "Basal: 40:60:50 NPK; 25 days: Urea; Silking: Small Urea.",
    "wheat": "Basal: DAP; 25 days: Urea; Heading: Light Urea.",
    "chilli": "Basal: 40 P + 40 K; Vegetative: Urea; Flowering: Potash.",
    "groundnut": "Gypsum + SSP recommended; Avoid excess nitrogen.",
}


# -----------------------------------------------------------
# SOIL TEST LOGIC
# -----------------------------------------------------------

def soil_test(n, p, k):
    n_stat = "Low" if n < 50 else "Medium" if n < 100 else "High"
    p_stat = "Low" if p < 40 else "Medium" if p < 80 else "High"
    k_stat = "Low" if k < 40 else "Medium" if k < 80 else "High"

    reply = f"""
🧪 **Soil Test Based Recommendation**

🔹 Nitrogen (N): {n_stat}  
🔹 Phosphorus (P): {p_stat}  
🔹 Potassium (K): {k_stat}  

"""

    if n_stat == "Low": reply += "➡ Apply Urea\n"
    if p_stat == "Low": reply += "➡ Apply DAP\n"
    if k_stat == "Low": reply += "➡ Apply MOP (Potash)\n"

    return reply


# -----------------------------------------------------------
# MAIN CHATBOT FUNCTION
# -----------------------------------------------------------

def chatbot_response(text):
    user = text.lower()

    # -------------------------------------
    # 1. FIRST TRY GOVERNMENT PDF RAG
    # -------------------------------------
    rag = rag_answer(user)
    if rag:
        return "📘 **Government Scheme Information:**\n" + "\n".join(rag)

    # -------------------------------------
    # 2. SEASONAL CROP QUESTIONS
    # -------------------------------------
    if "rainy" in user or "monsoon" in user or "వర్షాకాలం" in user:
        return "🌧️ **Rainy Season Best Crops:**\n- Paddy\n- Cotton\n- Maize\n- Turmeric\n- Soybean\n- Groundnut"

    if "summer" in user or "గ్రీష్మం" in user:
        return "☀️ **Summer Season Crops:**\n- Millets\n- Sunflower\n- Vegetables"

    if "winter" in user or "చలికాలం" in user:
        return "❄️ **Winter (Rabi) Crops:**\n- Wheat\n- Mustard\n- Barley"

    # -------------------------------------
    # 3. CROP DETAILS
    # -------------------------------------
    for crop in crop_info:
        if crop in user:
            return f"🌾 **{crop.capitalize()} Information:**\n{crop_info[crop]}\n\n💡 Fertilizer: {fertilizer_advice.get(crop, 'Data available')}"

    # -------------------------------------
    # 4. FERTILIZER ADVICE
    # -------------------------------------
    if "fertilizer" in user or "ఎరువు" in user:
        for crop in fertilizer_advice:
            if crop in user:
                return f"🌱 Fertilizer for {crop.capitalize()}:\n{fertilizer_advice[crop]}"

    # -------------------------------------
    # 5. SOIL TEST (NPK)
    # -------------------------------------
    if any(word in user for word in ["soil", "npk", "n ", "p ", "k "]):
        nums = re.findall(r"\d+", user)
        if len(nums) >= 3:
            n, p, k = map(int, nums[:3])
            return soil_test(n, p, k)
        return "Provide N, P, K values. Example: 'Soil N 40 P 20 K 10'"

    # -------------------------------------
    # 6. SCHEME QUESTIONS (BUILT-IN ANSWERS)
    # -------------------------------------
    if "pmbfy" in user or "pmfby" in user or "insurance" in user or "బీమా" in user:
        return (
            "🏛️ **PMFBY Crop Insurance:**\n"
            "- Farmers with land ownership are eligible\n"
            "- Premium: 2% Kharif, 1.5% Rabi\n"
            "- Covers natural calamity losses\n"
            "- Enrollment before sowing season"
        )

    if "rythu" in user or "bharosa" in user or "రైతు" in user:
        return (
            "💰 **YSR Rythu Bharosa:**\n"
            "- ₹13,500 yearly assistance\n"
            "- Paid in 3 installments\n"
            "- Land-owning farmers eligible"
        )

    if "pm kisan" in user or "kisan" in user:
        return (
            "🌿 **PM-KISAN Scheme:**\n"
            "- ₹6000/year\n"
            "- Direct bank transfer\n"
            "- All small & marginal farmers eligible"
        )

    # -------------------------------------
    # 7. FALLBACK: BASIC ASSISTANCE
    # -------------------------------------
    return (
        "🤖 నేను అర్థం చేసుకున్నాను.\n"
        "మీరు పంట పేరు, సీజన్, ఎరువు, పథకం గురించి అడగవచ్చు.\n\n"
        "You can ask about:\n"
        "- Best crop for season\n"
        "- Fertilizer advice\n"
        "- Soil test\n"
        "- Government schemes\n"
        "- Irrigation\n"
        "- Pests\n"
        "- Any crop details"
    )
