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
      
col1, col2 = st.columns(2)


prompt = col1.chat_input ("Say something")
if col2.button("🎙️ Speak"):
    transcription = recognize_speech()
    st.write("Transcription:", transcription)
    prompt=transcription
    st.write("You entered:", prompt)


if prompt:
    with st.chat_message("user"):
      st.write(prompt) 

# Create a form using st.form
with st.form(key='my_form'):
    # Display the chat-like input area with the default text
    user_input = st.text_area("Chat Input:", prompt, height=10)
    user_input2 = user_input
    st.write(user_input2)
    # Add a submit button to the form
    submit_button = st.form_submit_button(label='Submit')
    submit_button1 = st.form_submit_button("🎙️ Speak")
    

# Check if the form was submitted
if submit_button:
    # Display the entered text
    with st.chat_message("user"):
      st.write(user_input2)

if submit_button1:
    transcription = recognize_speech()
    user_input=transcription


if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.text_input("What is up?"):
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    # Display user message in chat message container
    with st.container():
        st.markdown(prompt)

# Place the voiceb button in the sidebar
voiceb = st.button("🎙️ Voice")
