import json
import uuid
from urllib.parse import unquote

import requests
import streamlit as st


API_URL = "http://127.0.0.1:8000/api/voice/quote-follow-up"
INITIAL_API_URL = "http://127.0.0.1:8000/api/voice/quote-follow-up/initial"


st.set_page_config(page_title="Voice Follow-up Test", page_icon="🎙️")
st.title("Voice Follow-up Test")

if "voice_session_id" not in st.session_state:
    st.session_state.voice_session_id = ""

initial_api_url = st.text_input("Initial API URL", INITIAL_API_URL)
api_url = st.text_input("Follow-up API URL", API_URL)
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

if st.button("Send initial voice", type="secondary"):
    active_session_id = session_id or st.session_state.voice_session_id or str(uuid.uuid4())
    form_data = {
        "session_id": active_session_id,
        "quote_data": quote_data_text,
    }

    with st.spinner("Sending initial voice request..."):
        response = requests.post(initial_api_url, data=form_data, timeout=120)

    if not response.ok:
        st.error(f"API error {response.status_code}: {response.text}")
        st.stop()

    new_session_id = response.headers.get("X-Voice-Session-Id", active_session_id)
    answer_text = unquote(response.headers.get("X-Voice-Text", ""))
    st.session_state.voice_session_id = new_session_id

    st.success("Initial voice response received.")
    st.audio(response.content, format="audio/mp3")
    st.caption(f"Session ID: {new_session_id}")
    st.text_area("Assistant text", answer_text, height=120)

if st.button("Send voice", type="primary"):
    active_session_id = session_id or st.session_state.voice_session_id
    if not active_session_id:
        st.warning("Send the initial voice first or enter a session ID.")
        st.stop()

    if audio_file is None:
        st.warning("Record or upload an audio file first.")
        st.stop()

    form_data = {
        "session_id": active_session_id,
    }

    files = {
        "audio": (
            audio_file.name or "voice-input.wav",
            audio_file.getvalue(),
            audio_file.type or "audio/wav",
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
