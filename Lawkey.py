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

