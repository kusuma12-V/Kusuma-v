import streamlit as st
from gtts import gTTS
import tempfile
import random
from streamlit_mic_recorder import mic_recorder

st.set_page_config(page_title="Krishi Sahay", layout="wide")

# -------------------- AUTO VOICE FUNCTION --------------------

def speak_auto(text, lang="en"):
    tts = gTTS(text=text, lang=lang)
    tmp = tempfile.NamedTemporaryFile(delete=False, suffix=".mp3")
    tts.save(tmp.name)
    audio_bytes = open(tmp.name, "rb").read()
    st.audio(audio_bytes, format="audio/mp3", autoplay=True)

# -------------------- SESSION STATE --------------------

if "page" not in st.session_state:
    st.session_state.page = "welcome"

if "otp" not in st.session_state:
    st.session_state.otp = None

# -------------------- WELCOME PAGE --------------------

if st.session_state.page == "welcome":

    if "spoken" not in st.session_state:
        speak_auto("Welcome to Krishi Sahay. Empowering farmers with smart agriculture technology.")
        st.session_state.spoken = True

    st.markdown("""
    <div style="
    background: linear-gradient(rgba(0,100,0,0.6), rgba(0,100,0,0.6)),
    url('https://images.unsplash.com/photo-1500937386664-56d1dfef3854');
    background-size: cover;
    background-position: center;
    padding:120px;
    border-radius:20px;
    text-align:center;
    color:white;">
    <h1 style="font-size:60px;">🌾 Krishi Sahay</h1>
    <h3>AI Powered Agriculture Assistant</h3>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<h2 style='text-align:center;'>Select Language</h2>", unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1,1,1])

    with col1:
        if st.button("English", key="eng"):
            st.session_state.language = "en"
            st.session_state.page = "login"

    with col2:
        if st.button("Kannada", key="kan"):
            st.session_state.language = "kn"
            st.session_state.page = "login"

    with col3:
        if st.button("Hindi", key="hin"):
            st.session_state.language = "hi"
            st.session_state.page = "login"

# -------------------- LOGIN PAGE --------------------

elif st.session_state.page == "login":

    st.markdown("## 🔐 Login to Krishi Sahay")

    name = st.text_input("Farmer Name")
    contact = st.text_input("Email or Mobile Number")

    if st.button("Generate OTP", key="genotp"):
        otp = random.randint(1000, 9999)
        st.session_state.otp = str(otp)
        st.success(f"Your OTP is: {otp} (Demo purpose)")

    entered_otp = st.text_input("Enter OTP")

    if st.button("Login", key="loginbtn"):
        if entered_otp == st.session_state.otp:
            st.session_state.user = name
            st.session_state.page = "dashboard"
        else:
            st.error("Invalid OTP")

# -------------------- DASHBOARD --------------------

elif st.session_state.page == "dashboard":

    st.markdown(f"# 🌿 Welcome {st.session_state.user}")

    col1, col2, col3 = st.columns(3)

    # -------- AI Assistant --------
    with col1:
        st.subheader("🤖 AI Assistant")
        question = st.text_input("Ask your question")
        if st.button("Get Answer", key="ai_answer"):
            answer = "Based on your query, proper irrigation and fertilizer management is recommended."
            st.success(answer)
            speak_auto(answer)

        audio = mic_recorder(key="mic1")
        if audio:
            st.info("Voice received (Speech-to-text integration needed here)")

    # -------- Crop Diagnosis --------
    with col2:
        st.subheader("🌾 Crop Diagnosis")
        image = st.file_uploader("Upload Crop Image", type=["jpg", "png"])
        if image:
            st.image(image, width=200)
            result = "The crop shows possible fungal infection. Apply recommended fungicide."
            st.success(result)
            speak_auto(result)

    # -------- Buyer Contact --------
    with col3:
        st.subheader("🛒 Buyer Contact")
        crop = st.text_input("Enter crop to sell")
        if st.button("Find Buyers", key="buyer"):
            st.success("Nearby buyer: Ramesh Traders, Bangalore, ₹2200/quintal")

    # -------- Government Schemes --------
    st.markdown("## 🏛 Government Schemes")
    scheme_query = st.text_input("Search Scheme")
    if st.button("Search Scheme", key="scheme"):
        st.success("PM-KISAN: ₹6000 yearly income support scheme.")

    # -------- Exit Button --------
    if st.button("🚪 Exit", key="exitbtn"):
        st.session_state.page = "thankyou"

# -------------------- THANK YOU PAGE --------------------

elif st.session_state.page == "thankyou":

    st.markdown("""
    <div style="
    background: linear-gradient(rgba(0,128,0,0.6), rgba(0,128,0,0.6)),
    url('https://images.unsplash.com/photo-1592982537447-7440770cbfc9');
    background-size: cover;
    background-position: center;
    padding:150px;
    border-radius:20px;
    text-align:center;
    color:white;">
    <h1>🌾 Thank You for Using Krishi Sahay</h1>
    <h3>Empowering Farmers with Smart Technology</h3>
    </div>
    """, unsafe_allow_html=True)

    if "bye_spoken" not in st.session_state:
        speak_auto("Thank you for using Krishi Sahay. Wishing you a healthy and profitable harvest.")
        st.session_state.bye_spoken = True

    if st.button("Back to Home", key="homebtn"):
        st.session_state.page = "welcome"