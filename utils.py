from openai import OpenAI
import base64
import streamlit as st
import os
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("openai_api_key")

client = OpenAI(api_key=api_key)

# Predefined responses to personal questions
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

    "What's one of the biggest challenges you've overcome?": 
        "Developing an AI-powered influencer-brand matching system at BrandCollab. "
        "Balancing business needs, technical constraints, and large-scale data processing was a huge learning experience.",

    "What advice would you give to someone starting in data science?": 
        "Get hands-on! Start with Python and statistics, but more importantly, build projects. "
        "Real-world experience is the best way to learn.",

    "What's your approach to problem-solving?": 
        "I break problems down into smaller components, analyze constraints, and experiment with solutions iteratively. "
        "Collaboration is also key—discussing ideas with others often leads to the best results.",

    "How do you stay updated with AI trends?": 
        "I follow research papers, attend conferences, contribute to open-source projects, and engage with the AI community. "
        "Staying ahead in AI means continuous learning!",

    "What excites you the most about AI and data science?": 
        "The ability to transform raw data into meaningful insights and real-world applications. "
        "AI is changing industries, and I love being part of that transformation."
}

def get_answer(messages):
    last_user_message = messages[-1]["content"].strip()

    # Check for predefined response
    if last_user_message in personal_responses:
        return personal_responses[last_user_message]

    # Enforce English and natural human-like responses
    system_message = [{"role": "system", "content": 
        "You will always respond as a real person, never as an AI. "
        "Speak naturally, as if you're having a personal conversation. "
        "All responses must be in English. If the input is not in English, politely ask the user to rephrase in English."
    }]

    messages = system_message + messages
    response = client.chat.completions.create(
        model="gpt-3.5-turbo-1106",
        messages=messages
    )
    return response.choices[0].message.content

def speech_to_text(audio_data):
    with open(audio_data, "rb") as audio_file:
        transcript = client.audio.transcriptions.create(
            model="whisper-1",
            response_format="text",
            file=audio_file,
            language="en"  # Ensuring English input
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