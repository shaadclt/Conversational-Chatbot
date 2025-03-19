import streamlit as st
import os
import base64
from openai import OpenAI, OpenAIError
from utils import get_answer, text_to_speech, autoplay_audio, speech_to_text
from audio_recorder_streamlit import audio_recorder
from streamlit_float import *

float_init()

# Function to validate OpenAI API Key
def validate_api_key(api_key):
    try:
        test_client = OpenAI(api_key=api_key)
        test_client.models.list()  # Test API access
        return True
    except OpenAIError:
        return False

# Sidebar for API Key input (only if not already stored)
if "openai_api_key" not in st.session_state:
    with st.sidebar:
        st.title("Configuration")
        openai_api_key = st.text_input("Enter your OpenAI API Key", type="password")

        if openai_api_key:
            if validate_api_key(openai_api_key):
                st.session_state["openai_api_key"] = openai_api_key
                st.session_state["sidebar_hidden"] = True  # Mark sidebar as hidden
                st.success("API Key is valid! Reloading...")
                st.rerun()
            else:
                st.error("Invalid OpenAI API Key. Please enter a valid key.")
                st.stop()

# Stop execution if API key is missing
if "openai_api_key" not in st.session_state:
    st.warning("Please enter a valid OpenAI API Key in the sidebar to continue.")
    st.stop()

# Hide Sidebar after valid key entry
if "sidebar_hidden" in st.session_state and st.session_state["sidebar_hidden"]:
    st.markdown(
        """
        <style>
        section[data-testid="stSidebar"] {display: none !important;}
        </style>
        """,
        unsafe_allow_html=True
    )

# Initialize OpenAI client with validated key
client = OpenAI(api_key=st.session_state["openai_api_key"])

# Chat Interface
def initialize_session_state():
    if "messages" not in st.session_state:
        st.session_state.messages = [
            {"role": "assistant", "content": "Hi! This is Mohamed Shaad. Ask me anything about my life, skills, or experiences!"}
        ]

initialize_session_state()

st.title("S Voice Chat")

footer_container = st.container()
with footer_container:
    audio_bytes = audio_recorder()

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

if audio_bytes:
    with st.spinner("Transcribing..."):
        webm_file_path = "temp_audio.mp3"
        with open(webm_file_path, "wb") as f:
            f.write(audio_bytes)

        transcript = speech_to_text(webm_file_path)
        if transcript:
            st.session_state.messages.append({"role": "user", "content": transcript})
            with st.chat_message("user"):
                st.write(transcript)
            os.remove(webm_file_path)

if st.session_state.messages[-1]["role"] != "assistant":
    with st.chat_message("assistant"):
        with st.spinner("Thinking🤔..."):
            final_response = get_answer(st.session_state.messages)
        with st.spinner("Generating audio response..."):    
            audio_file = text_to_speech(final_response)
            autoplay_audio(audio_file)
        st.write(final_response)
        st.session_state.messages.append({"role": "assistant", "content": final_response})
        os.remove(audio_file)

footer_container.float("bottom: 1rem;")



def set_bg_from_url(url, opacity=1):

    # Set background image using HTML and CSS
    st.markdown(
        f"""
        <style>
            body {{
                background: url('{url}') no-repeat center center fixed;
                background-size: cover;
                opacity: {opacity};
            }}
        </style>
        """,
        unsafe_allow_html=True
    )

# Set background image from URL
set_bg_from_url("https://www.cio.com/wp-content/uploads/2025/03/189347-0-57296500-1741174899-chatbot_ai_machine-learning_emerging-tech-100778305-orig.jpg?quality=50&strip=all", opacity=0.875)