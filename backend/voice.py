import streamlit as st
import speech_recognition as sr

r = sr.Recognizer()

# 🔥 Session state for recording
if "recording" not in st.session_state:
    st.session_state.recording = False

if "audio_data" not in st.session_state:
    st.session_state.audio_data = None


def start_recording():
    st.session_state.recording = True
    st.session_state.audio_data = None


def stop_recording():
    st.session_state.recording = False

    try:
        with sr.Microphone() as source:
            st.info("Processing audio...")
            audio = r.listen(source, timeout=5, phrase_time_limit=5)
            text = r.recognize_google(audio)

            st.session_state.text = text
            st.success(f"Recognized: {text}")

    except Exception as e:
        st.error(f"Error: {e}")

uvicorn backend.main:app
# 🔹 Buttons
col1, col2 = st.columns(2)

with col1:
    if st.button("🎤 Start Recording"):
        start_recording()

with col2:
    if st.button("⏹ Stop Recording"):
        stop_recording()