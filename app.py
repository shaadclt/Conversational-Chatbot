import streamlit as st
import os
import base64
from audio_recorder_streamlit import audio_recorder
from streamlit_float import *
from openai import OpenAI

# Float feature initialization
float_init()

# Initialize session state
if "api_key" not in st.session_state:
    st.session_state.api_key = ""

st.title("Conversational Chatbot")

# Function to validate API key
def validate_api_key(api_key):
    try:
        client = OpenAI(api_key=api_key)
        client.models.list()  # This is a simple call to list available models
        return True
    except Exception as e:
        return False

# API Key Input
if not st.session_state.api_key:
    api_key_input = st.text_input("Enter your OpenAI API key:", type="password")
    if api_key_input:
        if validate_api_key(api_key_input):
            st.session_state.api_key = api_key_input
            st.success("API key is valid!")
            st.rerun()  # Rerun the app to proceed to chat interface
        else:
            st.error("Invalid API key. Please try again.")
            st.stop()
    else:
        st.stop()

# Initialize OpenAI client with validated API key
client = OpenAI(api_key=st.session_state.api_key)

def initialize_session_state():
    if "messages" not in st.session_state:
        st.session_state.messages = [
            {"role": "assistant", "content": "Hi! How may I assist you today?"}
        ]

initialize_session_state()

personal_responses = {
"What should we know about your life story in a few sentences?":
"I'm a data scientist with a strong passion for NLP, generative AI, and MLOps. "
"I've worked on influencer-brand matching, AI chatbots, and various NLP applications. "
"I love solving real-world problems with data!",
"What is your number one superpower?":
"I have a knack for translating complex data science concepts into real-world applications. "
"Whether it's AI-driven recommendations or NLP solutions, I love making AI practical and impactful.",
"What are the top 3 areas you would like to grow in?":
"1. Enhancing my expertise in large-scale AI model deployment.\n"
"2. Expanding my knowledge of real-time recommendation systems.\n"
"3. Strengthening leadership and mentorship skills in AI teams.",
"What misconception do your coworkers have about you?":
"People sometimes assume I spend all my time coding, but I actually enjoy collaborating on AI strategies and brainstorming new ideas just as much.",
"How do you push your boundaries and limits?":
"I take on challenging AI projects, contribute to open-source, and stay updated with cutting-edge research. "
"I'm always looking for ways to improve and grow!",
"What motivates you every day?":
"The impact AI can have on the world excites me! "
"I love finding innovative solutions to complex problems and seeing my work make a difference.",
}

def get_answer(messages):
    last_user_message = messages[-1]["content"].strip()
    if last_user_message in personal_responses:
        return personal_responses[last_user_message]
    system_message = [{"role": "system", "content": 
        "You will always respond as a real person, never as an AI. "
        "Speak naturally, as if you're having a personal conversation. "
        "All responses must be in English. If the input is not in English, politely ask the user to rephrase in English."
    }]
    messages = system_message + messages
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=messages
    )
    return response.choices[0].message.content

def speech_to_text(audio_data):
    with open(audio_data, "rb") as audio_file:
        transcript = client.audio.transcriptions.create(
            model="whisper-1",
            file=audio_file,
            response_format="text",
            language="en"
        )
    return transcript

def text_to_speech(input_text):
    response = client.audio.speech.create(
        model="tts-1",
        voice="nova",
        input=input_text
    )
    webm_file_path = "temp_audio_play.mp3"
    with open(webm_file_path, "wb") as f:
        response.stream_to_file(webm_file_path)
    return webm_file_path

def autoplay_audio(file_path: str):
    with open(file_path, "rb") as f:
        data = f.read()
    b64 = base64.b64encode(data).decode("utf-8")
    md = f"""
    <audio autoplay>
    <source src="data:audio/mp3;base64,{b64}" type="audio/mp3">
    </audio>
    """
    st.markdown(md, unsafe_allow_html=True)

# Create footer container for the microphone
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

# Float the footer container
footer_container.float("bottom: 0rem;")

def set_bg_from_url(url, opacity=1):
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