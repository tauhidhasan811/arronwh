import json

import httpx
import streamlit as st


st.set_page_config(page_title="SSE Chat Client", page_icon=".", layout="centered")

st.title("SSE Chat Client")
st.caption("Send a message to the FastAPI `/chat/stream` endpoint and render tokens as they arrive.")

base_url = st.text_input("FastAPI base URL", value="http://127.0.0.1:8000")
message = st.text_area("Prompt", value="Write a short paragraph about cows.", height=140)

status_placeholder = st.empty()
output_placeholder = st.empty()


def parse_sse_event(raw_event: str) -> tuple[str, str] | None:
    lines = raw_event.splitlines()
    event_name = "message"
    data_lines: list[str] = []

    for line in lines:
        if line.startswith("event:"):
            event_name = line[6:].strip()
        elif line.startswith("data:"):
            data_lines.append(line[5:].strip())

    if not data_lines:
        return None

    return event_name, "\n".join(data_lines)


if st.button("Start Stream", type="primary"):
    full_text = ""
    status_placeholder.info("Connecting...")
    output_placeholder.markdown("")

    try:
        with httpx.stream(
            "POST",
            f"{base_url.rstrip('/')}/chat/stream",
            headers={"Content-Type": "application/json"},
            json={"message": message},
            timeout=60.0,
        ) as response:
            response.raise_for_status()
            buffer = ""

            for chunk in response.iter_text():
                buffer += chunk

                while "\n\n" in buffer:
                    raw_event, buffer = buffer.split("\n\n", 1)
                    parsed_event = parse_sse_event(raw_event)

                    if parsed_event is None:
                        continue

                    event_name, payload_text = parsed_event
                    payload = json.loads(payload_text)

                    if event_name == "start":
                        status_placeholder.info("Streaming...")
                    elif event_name == "token":
                        full_text += payload.get("content", "")
                        output_placeholder.markdown(full_text)
                    elif event_name == "done":
                        status_placeholder.success("Completed")
                    elif event_name == "error":
                        status_placeholder.error("Stream failed")
                        st.error(payload.get("error", "Unknown error"))

    except Exception as exc:
        status_placeholder.error("Connection failed")
        st.error(str(exc))
