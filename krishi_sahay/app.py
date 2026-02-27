import streamlit as st
from gtts import gTTS
import tempfile
import random
from groq import Groq

# 🔥 Add your Groq API Key
client = Groq(api_key="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")

st.set_page_config(page_title="Krishi Sahay", layout="wide")

# ---------------- GLOBAL STYLE ----------------
st.markdown("""
<style>

/* 🌾 Global font */
html, body, [class*="css"] {
    font-family: "Times New Roman", serif;
}

/* 🌾 Farmer background */
.stApp {
    background-image: url("https://images.unsplash.com/photo-1500937386664-56d1dfef3854");
    background-size: cover;
    background-attachment: fixed;
}

/* 🌾 3D green buttons */
div.stButton > button {
    height: 65px;
    font-size: 20px;
    font-weight: bold;
    background: linear-gradient(145deg, #0b8f3c, #38ef7d);
    color: white;
    border-radius: 10px;
    border: none;
    box-shadow: 4px 4px 10px #0a6f2d, -4px -4px 10px #4fff9c;
}

/* 🌾 Login box */
.login-box {
    background: rgba(0,80,0,0.85);
    padding: 40px;
    border-radius: 20px;
    color: white;
}

/* 🌾 Exit red button */
.exit button {
    background: red !important;
    color: white !important;
}

</style>
""", unsafe_allow_html=True)

# ---------------- LANGUAGE ----------------
language_map = {"en": "English", "kn": "Kannada", "hi": "Hindi"}

# ---------------- AI FUNCTION ----------------
def krishi_ai(question, lang_code):
    selected_language = language_map.get(lang_code, "English")

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {
                "role": "system",
                "content": f"You are an expert agriculture assistant. Give simple step-by-step farming advice. Reply strictly in {selected_language}."
            },
            {"role": "user", "content": question}
        ]
    )
    return response.choices[0].message.content


# ---------------- VOICE ----------------
def speak(text, lang):
    tts = gTTS(text=text, lang=lang)
    tmp = tempfile.NamedTemporaryFile(delete=False, suffix=".mp3")
    tts.save(tmp.name)
    audio = open(tmp.name, "rb").read()
    st.audio(audio, autoplay=True)


# ---------------- SESSION ----------------
if "page" not in st.session_state:
    st.session_state.page = "welcome"

if "otp" not in st.session_state:
    st.session_state.otp = None


# ================= WELCOME =================
# ================= WELCOME PAGE =================
elif st.session_state.page == "welcome":

    st.markdown("""
    <style>
    .welcome-box {
        background: linear-gradient(135deg, #4CAF50, #2e7d32);
        padding: 70px;
        border-radius: 25px;
        text-align: center;
        color: white;
        box-shadow: 0 0 30px rgba(0,0,0,0.4);
    }

    .main-title {
        font-size: 60px;
        font-weight: bold;
        font-family: 'Times New Roman';
        color: white;
    }

    .sub-title {
        font-size: 55px;
        font-weight: bold;
        color: black;   /* Krishi Sahay in dark color */
        margin-top: 15px;
    }

    .tag-line {
        font-size: 22px;
        margin-top: 20px;
    }
    </style>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="welcome-box">
        <div class="main-title">🌾 Welcome to Farmers World 🌾</div>
        <div class="sub-title">Krishi Sahay</div>
        <div class="tag-line">
            Smart AI Assistant for Modern Agriculture 🚜🌱
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<br><br>", unsafe_allow_html=True)

    col1, col2, col3 = st.columns([2,1,2])
    with col2:
        if st.button("🌿 Enter Dashboard"):
            st.session_state.page = "dashboard"
if st.session_state.page == "welcome":

    st.markdown("""
    <h1 style="
    text-align:center;
    font-family:'Times New Roman';
    font-weight:bold;
    font-size:75px;
    color:white;
    text-shadow:
        3px 3px 0px #0b8f3c,
        6px 6px 15px rgba(0,0,0,0.6);
    ">
    🌾 Krishi Sahay
    </h1>
    """, unsafe_allow_html=True)

    st.markdown("<h3 style='text-align:center;color:white;'>AI Powered Agriculture Assistant</h3>", unsafe_allow_html=True)
    st.markdown("### Select Language")

    if st.button("English"):
        st.session_state.language = "en"
        st.session_state.page = "login"

    if st.button("Kannada"):
        st.session_state.language = "kn"
        st.session_state.page = "login"

    if st.button("Hindi"):
        st.session_state.language = "hi"
        st.session_state.page = "login"

        


# ================= LOGIN =================
elif st.session_state.page == "login":

    st.markdown("<div class='login-box'>", unsafe_allow_html=True)

    st.markdown("## 🔐 Farmer Login")

    name = st.text_input("Farmer Name")
    contact = st.text_input("Mobile or Email")

    if st.button("Generate OTP"):
        otp = random.randint(1000, 9999)
        st.session_state.otp = str(otp)
        st.success(f"Demo OTP: {otp}")

    entered = st.text_input("Enter OTP")

    if st.button("Login"):
        if entered == st.session_state.otp:
            st.session_state.user = name
            st.session_state.page = "dashboard"
        else:
            st.error("Invalid OTP")

    st.markdown("</div>", unsafe_allow_html=True)


# ================= DASHBOARD =================
elif st.session_state.page == "dashboard":

    st.markdown(f"# 🌿 Welcome {st.session_state.user}")
    lang = st.session_state.language

    # ---------- AI Assistant ----------
    st.markdown("## 🤖 AI Agriculture Assistant")
    question = st.text_input("Ask your farming question")

    if st.button("Get Answer"):
        if question:
            answer = krishi_ai(question, lang)
            st.success(answer)
            speak(answer, lang)

    # ---------- Voice demo ----------
    if st.button("🎤 Voice Assistant"):
        st.info("Voice feature ready for demo.")

    st.markdown("---")

    # ---------- Crop Diagnosis ----------
    st.markdown("## 🌾 Crop Diagnosis")
    img = st.file_uploader("Upload crop image", type=["jpg", "png", "jpeg"])

    if img:
        st.image(img, width=250)
        result = krishi_ai("Suggest possible crop disease and treatment.", lang)
        st.success(result)
        speak(result, lang)

    st.markdown("---")

    # ---------- Buyer ----------
    st.markdown("## 🛒 Buyer Contact")
    crop = st.text_input("Enter crop to sell")

    if st.button("Find Buyers"):
        buyer = krishi_ai(f"Give Karnataka buyers and price for {crop}.", lang)
        st.success(buyer)

    st.markdown("---")

    # ---------- Schemes ----------
    st.markdown("## 🏛 Government Schemes")
    scheme = st.text_input("Search scheme")

    if st.button("Search"):
        scheme_ans = krishi_ai(f"Explain Indian farmer schemes for {scheme}.", lang)
        st.success(scheme_ans)

    st.markdown("---")

    # ---------- EXIT CENTER RED ----------
    col1, col2, col3 = st.columns([2,1,2])
    with col2:
        if st.button("Exit"):
            st.session_state.page = "thankyou"


# ================= THANK YOU =================
elif st.session_state.page == "thankyou":

    st.markdown("""
    <style>
    .thank-box {
        background: rgba(0, 100, 0, 0.85);
        padding: 60px;
        border-radius: 25px;
        text-align: center;
        color: white;
        box-shadow: 0 0 25px rgba(0,255,0,0.6);
    }

    .thank-title {
        font-family: 'Times New Roman';
        font-size: 65px;
        font-weight: bold;
        text-shadow:
            3px 3px 0px #0b8f3c,
            6px 6px 15px rgba(0,0,0,0.6);
    }

    .thank-sub {
        font-size: 22px;
        margin-top: 20px;
    }
    </style>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="thank-box">
        <div class="thank-title">🌾 Thank You for Using Krishi Sahay 🌾</div>
        <div class="thank-sub">
            Empowering Farmers with Smart AI Technology<br><br>
            🌱 May your crops be healthy<br>
            💰 May your harvest be profitable<br>
            🌦 May your seasons be favorable
        </div>
    </div>
    """, unsafe_allow_html=True)
    # Optional voice message
    if "bye_spoken" not in st.session_state:
        speak("Thank you for using Krishi Sahay. Wishing you healthy crops and prosperous harvest.", 
              st.session_state.language)
        st.session_state.bye_spoken = True

    st.markdown("<br><br>", unsafe_allow_html=True)

    # Centered Back Button
    col1, col2, col3 = st.columns([2,1,2])
    with col2:
        if st.button("🌿 Back to Home"):
            st.session_state.page = "welcome"

    