import json
from urllib.parse import unquote

import requests
import streamlit as st


API_URL = "http://127.0.0.1:8000/api/voice/quote-follow-up"


st.set_page_config(page_title="Voice Follow-up Test", page_icon="🎙️")
st.title("Voice Follow-up Test")

if "voice_session_id" not in st.session_state:
    st.session_state.voice_session_id = ""

api_url = st.text_input("API URL", API_URL)
session_id = st.text_input("Session ID", st.session_state.voice_session_id)

quote_data_text = st.text_area(
    "Quote data",
    value=json.dumps(
        {
            "customer_name": "Test User",
            "quote_status": "created_not_purchased",
            "boiler": "Combi boiler",
            "estimated_price": "Not confirmed",
            "postcode": "SW1A 1AA",
        },
        indent=2,
    ),
    height=180,
)

audio_value = st.audio_input("Record customer voice")
uploaded_audio = st.file_uploader(
    "Or upload an audio file",
    type=["webm", "wav", "mp3", "m4a", "ogg"],
)

audio_file = audio_value or uploaded_audio

if st.button("Send voice", type="primary"):
    if audio_file is None:
        st.warning("Record or upload an audio file first.")
        st.stop()

    form_data = {
        "quote_data": quote_data_text,
    }
    if session_id:
        form_data["session_id"] = session_id

    files = {
        "audio": (
            audio_file.name or "voice-input.webm",
            audio_file.getvalue(),
            audio_file.type or "application/octet-stream",
        )
    }

    with st.spinner("Sending voice to API..."):
        response = requests.post(api_url, data=form_data, files=files, timeout=120)

    if not response.ok:
        st.error(f"API error {response.status_code}: {response.text}")
        st.stop()

    new_session_id = response.headers.get("X-Voice-Session-Id", "")
    transcript = unquote(response.headers.get("X-Voice-Transcript", ""))
    answer_text = unquote(response.headers.get("X-Voice-Text", ""))

    if new_session_id:
        st.session_state.voice_session_id = new_session_id

    st.success("Voice response received.")
    st.audio(response.content, format="audio/mp3")

    st.caption(f"Session ID: {new_session_id}")
    st.text_area("Transcript", transcript, height=90)
    st.text_area("Assistant text", answer_text, height=120)
