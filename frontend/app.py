import streamlit as st
import requests
import speech_recognition as sr
import cv2
import numpy as np
import pyautogui

# 🔥 PAGE CONFIG
st.set_page_config(layout="wide", initial_sidebar_state="expanded")

# 🔥 CLEAN UI CSS (FIXED)
st.markdown("""
<script>
const openSidebar = () => {
    const btn = window.parent.document.querySelector('[data-testid="collapsedControl"]');
    if (btn) {
        btn.click();
    }
};

// Try multiple times (Streamlit load delay fix)
setTimeout(openSidebar, 500);
setTimeout(openSidebar, 1000);
setTimeout(openSidebar, 2000);
</script>
""", unsafe_allow_html=True)

# 🔐 STATES
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "page" not in st.session_state:
    st.session_state.page = "login"

if "users" not in st.session_state:
    st.session_state.users = {"admin": "1234"}

# 🔐 LOGIN
def login():
    col1, col2, col3 = st.columns([1,2,1])
    with col2:
        st.markdown("## 🔐 Login")

        username = st.text_input("Username")
        password = st.text_input("Password", type="password")

        b1, b2, b3 = st.columns(3)

        with b1:
            if st.button("Login"):
                if username in st.session_state.users and st.session_state.users[username] == password:
                    st.session_state.logged_in = True
                    st.rerun()
                else:
                    st.error("Invalid username/password")

        with b2:
            if st.button("Register"):
                st.session_state.page = "register"
                st.rerun()

        with b3:
            if st.button("Forgot"):
                st.session_state.page = "forgot"
                st.rerun()

# 📝 REGISTER
def register():
    col1, col2, col3 = st.columns([1,2,1])
    with col2:
        st.markdown("## 📝 Register")

        new_user = st.text_input("New Username")
        new_pass = st.text_input("New Password", type="password")

        if st.button("Create Account"):
            if new_user in st.session_state.users:
                st.warning("User exists")
            elif new_user and new_pass:
                st.session_state.users[new_user] = new_pass
                st.success("Account created ✅")
                st.session_state.page = "login"
                st.rerun()

        if st.button("Back"):
            st.session_state.page = "login"
            st.rerun()

# 🔑 FORGOT
def forgot():
    col1, col2, col3 = st.columns([1,2,1])
    with col2:
        st.markdown("## 🔑 Reset Password")

        username = st.text_input("Username")
        new_pass = st.text_input("New Password", type="password")

        if st.button("Reset"):
            if username in st.session_state.users:
                st.session_state.users[username] = new_pass
                st.success("Updated ✅")
                st.session_state.page = "login"
                st.rerun()
            else:
                st.error("User not found")

        if st.button("Back"):
            st.session_state.page = "login"
            st.rerun()

# 🚨 PAGE SWITCH
if not st.session_state.logged_in:
    if st.session_state.page == "login":
        login()
    elif st.session_state.page == "register":
        register()
    else:
        forgot()
    st.stop()

# 🔥 MAIN APP
st.title("🧠 RecallX AI Brain")

# 🔥 SIDEBAR
st.sidebar.title("📊 Dashboard")

# 🎥 Screen Record States
if "recording" not in st.session_state:
    st.session_state.recording = False

st.subheader("🎥 Screen Recorder")

col1, col2 = st.columns(2)

# ▶️ START
with col1:
    if st.button("▶️ Start Recording"):
        st.session_state.recording = True
        st.success("Recording Started")

# ⏹ STOP
with col2:
    if st.button("⏹ Stop Recording"):
        st.session_state.recording = False
        st.warning("Recording Stopped")

# 🎬 RECORD LOGIC
if st.session_state.recording:

    screen_size = pyautogui.size()

    fourcc = cv2.VideoWriter_fourcc(*"XVID")
    out = cv2.VideoWriter("output.avi", fourcc, 10.0, screen_size)

    st.info("Recording in background...")

    for i in range(100):  # 100 frames approx (short demo)
        img = pyautogui.screenshot()
        frame = np.array(img)
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        out.write(frame)

    out.release()
    st.success("Saved as output.avi ✅")

menu = st.sidebar.radio(
    "",
    ["💬 Chat", "📝 Memory", "🔍 Search", "🚪 Logout"]
)

# 🚪 LOGOUT
if menu == "🚪 Logout":
    st.session_state.logged_in = False
    st.session_state.page = "login"
    st.rerun()

# 🔥 SESSION
if "messages" not in st.session_state:
    st.session_state.messages = []

if "text" not in st.session_state:
    st.session_state.text = ""

r = sr.Recognizer()

# 🎤 VOICE
def record():
    try:
        with sr.Microphone() as src:
            st.info("🎤 Listening...")
            audio = r.listen(src)
            return r.recognize_google(audio)
    except:
        return ""

# 💬 CHAT
if menu == "💬 Chat":
    st.subheader("💬 Chat")

    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.write(msg["content"])

    user_input = st.chat_input("Ask something...")

    if user_input:
        st.session_state.messages.append({"role": "user", "content": user_input})

        try:
            res = requests.post(
                "http://127.0.0.1:8000/chat",
                params={"query": user_input}
            )
            response = res.json().get("answer", "Error")
        except:
            response = "Backend not running ❌"

        st.session_state.messages.append({"role": "assistant", "content": response})
        st.rerun()

# 📝 MEMORY
elif menu == "📝 Memory":
    st.subheader("📝 Add Memory")

    st.session_state.text = st.text_area("Enter Memory", value=st.session_state.text)

    if st.button("💾 Save"):
        if st.session_state.text:
            try:
                requests.post(
                    "http://127.0.0.1:8000/add",
                    json={"text": st.session_state.text}
                )
                st.success("Saved ✅")
                st.session_state.text = ""
            except:
                st.error("Backend not running ❌")

# 🔍 SEARCH (🔥 FIXED)
elif menu == "🔍 Search":
    st.subheader("🔍 Smart Search")

    query = st.text_input("Search your memory...")

    if query:
        try:
            res = requests.get("http://127.0.0.1:8000/memories")
            data = res.json()

            found = False

            for item in data:
                if query.lower() in item["content"].lower():
                    st.success(item["content"])
                    found = True

            if not found:
                st.warning("No results found")

        except:
            st.error("⚠️ Backend not running! Run FastAPI first")