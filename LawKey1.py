import io
import tempfile

import requests
import streamlit as st
import speech_recognition as sr
from gtts import gTTS
import run


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


def text_to_speech(text):
    tts = gTTS(text=text, lang='en')
    return tts


# function to play the speech
def play_speech(tts):
    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as temp_audio:
        tts.save(temp_audio.name)
        st.audio(temp_audio.name, format='audio/mp3')


def signin():
    with st.form(key='signin', clear_on_submit=True):
        username = st.text_input(':blue[User Name]', placeholder='Enter a user name')
        password = st.text_input(':blue[Password]', placeholder="Enter Your Password", type='password')
        btns1, btns2, btns3, btns4, btns5 = st.columns(5)
        with btns3:
            st.form_submit_button('Sign Up')


def homepage():
    bt1, bt2, bt3, bt4 = st.columns(4)
    if bt4.button('Already a Member?'):
        signin()
    with st.form(key='signup', clear_on_submit=True):
        st.subheader('Sign Up')
        name = st.text_input(':blue[Name]', placeholder='Enter your name')
        username1 = st.text_input(':blue[User Name]', placeholder='Enter a user name')
        password1 = st.text_input(':blue[Password]', placeholder="Enter Your Password", type='password')
        password2 = st.text_input(':blue[Confirm Password]', placeholder=" Re Enter Your Password", type='password')

        btn1, btn2, btn3, btn4, btn5 = st.columns(5)
        with btn3:
            st.form_submit_button('Sign Up')


def chatbot():
    st.title("LAW-Key")

    with st.sidebar:
        with st.container(height=300):
            st.text("history")

    recognized_text = st.chat_input("Say something")
    button_pressed = False
    col1, col2 = st.columns(2)
    # Check if "🎙️ Speak" button is clicked
    if col1.button("🎙️ voice "):
        transcription = recognize_speech()
        recognized_text = transcription
    # Check if "Press Me" button is pressed
    if col2.button(":loud_sound: speaker"):
        button_pressed = True

    if "messages" not in st.session_state:
        st.session_state.messages = []
    if "voice" not in st.session_state:
        st.session_state.voice = ""
    if 'session_data' not in st.session_state:
        st.session_state.session_data = []

    if recognized_text:
        st.session_state.voice = recognized_text
        with st.container():
            st.session_state.messages.append({"role": "user", "content": recognized_text})
            response, similarity, mapping, similar_state, q_table, query = run.main(recognized_text)
            st.session_state.session_data.append(
                {'query': query, 'similar_state': similar_state, 'response': response, 'similarity': similarity,
                 'mapping': mapping, 'q_table': q_table})
            st.session_state.messages.append({"role": "AI", "content": response})
            st.session_state.voice = response
    if not st.session_state.messages:
        with st.chat_message("ai"):
            st.write("Hello 👋")
    else:
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])
        st.write('please give a feedback for the response')
        emoji_positive = "😃"
        emoji_neutral = "😐"
        emoji_negative = "😢"

        # Handle button clicks
        emcol1, emcol2, emcol3, emcol4, emcol5, emcol6, emcol7, emcol8, emcol9 = st.columns(9)
        if emcol1.button(emoji_positive, key="positive_button"):
            feedback = 1
            last_data = st.session_state.session_data[-1]

            # Assigning  individual variables from the last data
            query = last_data['query']
            similar_state = last_data['similar_state']
            response = last_data['response']
            similarity = last_data['similarity']
            mapping = last_data['mapping']
            q_table = last_data['q_table']
            save = run.save(query, similar_state, response, feedback, similarity, mapping, q_table)

        if emcol2.button(emoji_neutral, key="neutral_button"):
            feedback = 0
            last_data = st.session_state.session_data[-1]

            # Assigning  individual variables from the last data
            query = last_data['query']
            similar_state = last_data['similar_state']
            response = last_data['response']
            similarity = last_data['similarity']
            mapping = last_data['mapping']
            q_table = last_data['q_table']
            save = run.save(query, similar_state, response, feedback, similarity, mapping, q_table)

        if emcol3.button(emoji_negative, key="negative_button"):
            feedback = -1
            last_data = st.session_state.session_data[-1]

            # Assigning  individual variables from the last data
            query = last_data['query']
            similar_state = last_data['similar_state']
            response = last_data['response']
            similarity = last_data['similarity']
            mapping = last_data['mapping']
            q_table = last_data['q_table']
            save = run.save(query, similar_state, response, feedback, similarity, mapping, q_table)

    if button_pressed:
        tts2 = text_to_speech(st.session_state.voice)
        play_speech(tts2)


def account():
    st.title("Account")


def helpu():
    st.title("how can we help")


def about_us():
    st.title("We are ")


def main():
    st.sidebar.title("Navigation")
    page_options = ["Sign up", "chatbot", "Account", "About us", "Help"]
    selected_page = st.sidebar.selectbox("Select Page", page_options)

    if selected_page == "Sign up":
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
