import io
import tempfile

import requests
import streamlit as st
import speech_recognition as sr
from gtts import gTTS
import pyttsx3


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


def speak_text(text):
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()


def text_to_speech(text):
    tts = gTTS(text=text, lang='en')
    return tts


# function to play the speech
def play_speech(tts):
    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as temp_audio:
        tts.save(temp_audio.name)
        st.audio(temp_audio.name, format='audio/mp3')


def homepage():
    st.title("Home Page")
    st.write("Welcome to the Home Page!")


def chatbot():
    st.title("LAW-Key")

    with st.sidebar:
        with st.container(height=300):
            st.text("history")

    recognized_text = st.chat_input("Say something")
    button_pressed = False
    col1 , col2 = st.columns(2)
    # Check if "🎙️ Speak" button is clicked
    if col1.button("🎙️ "):
        transcription = recognize_speech()
        recognized_text = transcription
    # Check if "Press Me" button is pressed
    if col2.button(":loud_sound:"):
        button_pressed = True

    with st.chat_message("ai"):
        st.write("Hello 👋")

    if "messages" not in st.session_state:
        st.session_state.messages = []
    if "voice" not in st.session_state:
        st.session_state.voice = ""

    if recognized_text:
        st.session_state.voice = recognized_text
        with st.container():
            st.session_state.messages.append({"role": "user", "content": recognized_text})
            # rasa_output = interact_with_rasa(recognized_text.text_input)
            # for response in rasa_output:
            #     st.session_state.messages.append({"role": "AI", "content": response.get("text", "")})

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    if button_pressed:
        tts2 = text_to_speech(st.session_state.voice)
        play_speech(tts2)


def account():
    st.title("Account")
    st.write("Welcome to the Home Page!")

    # Initialize the text-to-speech engine
    engine = pyttsx3.init()

    # Function to speak the given text
    def speak(text):
        engine.say(text)
        engine.runAndWait()

    # Sample text (replace this with your variable)
    text_to_speak = "Hello, this is a sample text ."

    # Generate the speech and play it
    if st.button("test"):
        speak(text_to_speak)


def helpu():
    st.title("how can we help")


def about_us():
    st.title("We are ")


def main():
    st.sidebar.title("Navigation")
    page_options = ["Home", "chatbot", "Account", "About us", "Help"]
    selected_page = st.sidebar.selectbox("Select Page", page_options)

    if selected_page == "Home":
        homepage()
    elif selected_page == "chatbot":
        chatbot()
    elif selected_page == "Account":
        account()
    elif selected_page == "About us":
        about_us()
    elif selected_page == "Help":
        helpu()


if __name__ == "__main__":
    main()
