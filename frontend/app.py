import streamlit as st
import requests
import speech_recognition as sr

st.set_page_config(layout="wide")
st.title("RecallX AI Brain 🧠")

# 🔥 Session state
if "messages" not in st.session_state:
    st.session_state.messages = []

if "text" not in st.session_state:
    st.session_state.text = ""

r = sr.Recognizer()

# 🔥 Voice
def record():
    try:
        with sr.Microphone() as src:
            st.info("Listening...")
            audio = r.listen(src)
            return r.recognize_google(audio)
    except Exception as e:
        st.error(f"Voice error: {e}")
        return ""

# 🔥 Chat Display
st.subheader("💬 Chat")

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

# 🔥 Input
user_input = st.chat_input("Ask something...")

if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})

    # Call backend
    try:
        res = requests.post(
            "http://127.0.0.1:8000/chat",
            params={"query": user_input}
        )
        response = res.json().get("response", "Error")

    except Exception as e:
        response = f"Error: {e}"

    st.session_state.messages.append({"role": "assistant", "content": response})

    st.rerun()

# 🔥 Divider
st.divider()

# 🔥 MEMORY SAVE SECTION
st.subheader("📝 Add Memory")

st.session_state.text = st.text_area(
    "Enter Memory",
    value=st.session_state.text
)

col1, col2 = st.columns(2)

# 🎤 Voice
with col1:
    if st.button("🎤 Voice"):
        voice_text = record()
        if voice_text:
            st.session_state.text = voice_text

# 💾 Save
with col2:
    if st.button("Save"):
        if st.session_state.text:
            try:
                res = requests.post(
                    "http://127.0.0.1:8000/add",
                    json={"text": st.session_state.text}
                )
                st.success("Saved ✅")
                st.session_state.text = ""
            except Exception as e:
                st.error(f"Error: {e}")
        else:
            st.warning("Enter text first")

# 🔥 AUTO SUGGESTION SEARCH
st.divider()
st.subheader("🔍 Smart Search")

query = st.text_input("Type to search...")

if query:
    try:
        res = requests.get(
            "http://127.0.0.1:8000/search",
            params={"query": query}
        )
        data = res.json()

        for item in data[:3]:  # top suggestions
            st.write("💡", item["content"])

    except Exception as e:
        st.error(f"Error: {e}")