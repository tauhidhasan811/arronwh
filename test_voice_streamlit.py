import json
import uuid
from urllib.parse import unquote

import requests
import streamlit as st

API_URL = "http://127.0.0.1:8000/api/voice/quote-follow-up"
INITIAL_API_URL = "http://127.0.0.1:8000/api/voice/quote-follow-up/initial"

st.set_page_config(
    page_title="Voice Follow-up Test",
    page_icon="🎙️",
    layout="wide"
)

st.title("🎙️ Voice Follow-up Test")

if "voice_session_id" not in st.session_state:
    st.session_state.voice_session_id = str(uuid.uuid4())

initial_api_url = st.text_input(
    "Initial API URL",
    INITIAL_API_URL
)

api_url = st.text_input(
    "Follow-up API URL",
    API_URL
)

session_id = st.text_input(
    "Session ID",
    st.session_state.voice_session_id
)

quote_data_text = st.text_area(
    "Quote Data",
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
    height=220,
)

audio_value = st.audio_input("Record customer voice")

uploaded_audio = st.file_uploader(
    "Or Upload Audio",
    type=["webm", "wav", "mp3", "m4a", "ogg"],
)

audio_file = audio_value or uploaded_audio

col1, col2 = st.columns(2)

# ---------------- INITIAL MESSAGE ---------------- #

with col1:
    if st.button("Send Initial Voice"):

        active_session_id = (
            session_id
            or st.session_state.voice_session_id
            or str(uuid.uuid4())
        )

        headers = {
            "X-Voice-Session-Id": active_session_id
        }

        form_data = {
            "quote_data": quote_data_text
        }

        try:
            with st.spinner("Generating initial response..."):
                response = requests.post(
                    initial_api_url,
                    headers=headers,
                    data=form_data,
                    timeout=120,
                )

            if not response.ok:
                st.error(
                    f"API error {response.status_code}: {response.text}"
                )
                st.stop()

            returned_session_id = response.headers.get(
                "X-Voice-Session-Id",
                active_session_id,
            )

            answer_text = unquote(
                response.headers.get(
                    "X-Voice-Text",
                    "",
                )
            )

            st.session_state.voice_session_id = (
                returned_session_id
            )

            st.success("Initial response received")

            st.audio(
                response.content,
                format="audio/mp3",
            )

            st.caption(
                f"Session ID: {returned_session_id}"
            )

            st.text_area(
                "Assistant Response",
                answer_text,
                height=150,
            )

        except Exception as e:
            st.error(str(e))

# ---------------- FOLLOW-UP MESSAGE ---------------- #

with col2:
    if st.button("Send Voice"):

        active_session_id = (
            session_id
            or st.session_state.voice_session_id
        )

        if not active_session_id:
            st.warning(
                "Send initial voice first or enter a session ID."
            )
            st.stop()

        if audio_file is None:
            st.warning(
                "Please record or upload an audio file."
            )
            st.stop()

        headers = {
            "X-Voice-Session-Id": active_session_id
        }

        files = {
            "audio": (
                getattr(audio_file, "name", "voice-input.wav"),
                audio_file.getvalue(),
                getattr(audio_file, "type", "audio/wav"),
            )
        }

        try:
            with st.spinner("Sending audio..."):
                response = requests.post(
                    api_url,
                    headers=headers,
                    files=files,
                    timeout=120,
                )

            if not response.ok:
                st.error(
                    f"API error {response.status_code}: {response.text}"
                )
                st.stop()

            returned_session_id = response.headers.get(
                "X-Voice-Session-Id",
                active_session_id,
            )

            transcript = unquote(
                response.headers.get(
                    "X-Voice-Transcript",
                    "",
                )
            )

            answer_text = unquote(
                response.headers.get(
                    "X-Voice-Text",
                    "",
                )
            )

            st.session_state.voice_session_id = (
                returned_session_id
            )

            st.success("Voice response received")

            st.audio(
                response.content,
                format="audio/mp3",
            )

            st.caption(
                f"Session ID: {returned_session_id}"
            )

            st.text_area(
                "Transcript",
                transcript,
                height=120,
            )

            st.text_area(
                "Assistant Response",
                answer_text,
                height=150,
            )

        except Exception as e:
            st.error(str(e))