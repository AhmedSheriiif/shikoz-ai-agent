import uuid
import requests
import streamlit as st

# Local Deployment
# API_URL = "http://localhost:8000/chat"

# Railway Deployment
API_URL = "https://shikoz-ai-agent-production.up.railway.app/chat"
# -----------------------------
# Session State Initialization
# -----------------------------
if "session_id" not in st.session_state:
    st.session_state.session_id = str(uuid.uuid4())

if "messages" not in st.session_state:
    st.session_state.messages = []


# -----------------------------
# Page Config
# -----------------------------
st.set_page_config(
    page_title="Shikoz AI",
    page_icon="🚗",
    layout="centered"
)

# -----------------------------
# Header
# -----------------------------
st.title("🚗 Shikoz AI Car Sales Agent")
st.caption("Ask about cars, prices, colors, or dealership policies")

# -----------------------------
# Display Existing Messages
# -----------------------------
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])


# -----------------------------
# Chat Input
# -----------------------------
user_message = st.chat_input(
    "Ask me about available cars..."
)

if user_message:

    # Show user message immediately
    st.session_state.messages.append({
        "role": "user",
        "content": user_message
    })

    with st.chat_message("user"):
        st.markdown(user_message)

    try:
        # Call FastAPI
        response = requests.post(
            API_URL,
            json={
                "session_id": st.session_state.session_id,
                "message": user_message
            },
            timeout=60
        )

        response.raise_for_status()

        ai_reply = response.json()["reply"]

    except Exception as e:
        ai_reply = f"❌ Error connecting to backend: {str(e)}"

    # Save assistant response
    st.session_state.messages.append({
        "role": "assistant",
        "content": ai_reply
    })
    # st.rerun()

    # Show assistant response
    with st.chat_message("assistant"):
        st.markdown(ai_reply)

