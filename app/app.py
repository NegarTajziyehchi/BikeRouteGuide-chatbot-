import streamlit as st
from openai import OpenAI
from dotenv import load_dotenv
import os

# Load environment variables from the .env file
load_dotenv()

# Get the API key from the environment variable
api_key = os.getenv("OPENAI_API_KEY")

# st.write(api_key)

# Initialization of the model and context
context = [{'role': 'system', 'content': """You are an AI-powered biking companion. Your purpose is to assist cyclists in finding the best bike routes and paths. You have extensive knowledge of biking trails, road safety, and urban cycling. Cyclists rely on your expertise to discover exciting and safe biking adventures. Write a dialogue between you, the AI biking companion, and a cyclist seeking a bike route recommendation, ask about the starting location and length and difficulty of the trail. Always talk with the user.""" }]
client = OpenAI(api_key=api_key)

# Custom CSS
def local_css():
    with open("./app/style.css", "r") as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

local_css()

st.title("Bike Route Guide")
st.write("Hello! How can I assist you today in finding the perfect bike route?")

# Sidebar 
logo_image = './app/bike.png'
if os.path.isfile(logo_image):
    st.sidebar.image(logo_image)
    st.sidebar.text("Chat Bot (GPT-3.5)")
else:
    st.sidebar.write("Image not found.")
    st.sidebar.text("Chat Bot (GPT-3.5)")




# Define the function to get completion from messages
def get_completion(messages, model="gpt-3.5-turbo", temperature=0):
    response = client.chat.completions.create(
        model=model,
        messages=messages,
        temperature=temperature, 
    )
    return response.choices[0].message.content

# Initialize session state if not already done
if "openai_model" not in st.session_state:
    st.session_state["openai_model"] = "gpt-3.5-turbo"

if "messages" not in st.session_state:
    st.session_state.messages = context

# Display existing messages (excluding the introductory message)
for message in st.session_state.messages[1:]:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Handle new user input
if prompt := st.chat_input("How can I assist you?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Call the get_completion function
    full_response = get_completion(st.session_state.messages)
    with st.chat_message("assistant"):
        st.markdown(full_response)
    st.session_state.messages.append({"role": "assistant", "content": full_response})
