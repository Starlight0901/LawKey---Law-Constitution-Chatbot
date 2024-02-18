import streamlit as st

# Check if the "messages" key exists in session_state
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Create a form for user input
user_input_form = st.form(key='user_input_form')

# Accept user input
with user_input_form:
    prompt = st.text_input("What is up?")
    submit_button = st.form_submit_button(label='Submit')

# Check if the form was submitted
if submit_button:
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})

# Display user message in chat message container
with st.chat_message("user"):
    st.markdown(prompt)






import streamlit as st
import speech_recognition as sr
from io import BytesIO
from PIL import Image

def recognize_speech():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Say something:")
        audio = recognizer.listen(source)

    try:
        return recognizer.recognize_google(audio)
    except sr.UnknownValueError:
        print("Could not understand audio.")
    except sr.RequestError as e:
        print(f"Error making a request to Google API: {e}")


st.title("LAW-Key")
    
with st.sidebar:    
    with st.container(height=300):
        st.text("history")

with st.chat_message("ai"):
      st.write("Hello 👋")

prompt = st.chat_input ("Say something")
if st.button("🎙️ Speak"):
    transcription = recognize_speech()
    prompt=transcription
    
if "messages" not in st.session_state:
    st.session_state.messages = []

if prompt :
    # Display user message in chat message container
    with st.container():
        st.session_state.messages.append({"role": "user", "content": prompt})
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])        

