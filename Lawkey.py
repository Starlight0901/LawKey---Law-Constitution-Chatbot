import streamlit as st
import speech_recognition as sr
from io import BytesIO
from PIL import Image
import requests

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

def interact_with_rasa(input):
    rasa_server_url = "http://localhost:5005/webhooks/rest/webhook"
    payload = {"sender": "streamlit_user", "message": input}
    response = requests.post(rasa_server_url, json=payload)
    return response.json()

st.title("LAW-Key")
    
with st.sidebar:    
    with st.container(height=300):
        st.text("history")
prompt = st.chat_input ("Say something")
if st.button("🎙️ Speak"):
    transcription = recognize_speech()
    prompt = transcription
    
with st.chat_message("ai"):
      st.write("Hello 👋")



    
if "messages" not in st.session_state:
    st.session_state.messages = []

if prompt :
    # Display user message in chat message container
    with st.container():
        st.session_state.messages.append({"role": "user", "content": prompt})
        rasa_output = interact_with_rasa(prompt)
        for response in rasa_output:
            st.session_state.messages.append({"role": "ai", "content": response.get("text", "")})

   
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])        
