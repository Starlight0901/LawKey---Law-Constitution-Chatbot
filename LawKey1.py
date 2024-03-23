import io
import tempfile
import firebase_admin
from firebase_admin import credentials
from firebase_admin import auth
import requests
import streamlit as st
import speech_recognition as sr
from gtts import gTTS
import run
import pyrebase

# fire base configuration
creden = credentials.Certificate('lawkey-561f0-54b1d35f6611.json')

config = {
    "apiKey": "AIzaSyDt4EqnrB2clEi1G2Mf_5OIyV9c2lfgE9M",
    "authDomain": "lawkey-561f0.firebaseapp.com",
    "databaseURL": "https://lawkey-561f0-default-rtdb.asia-southeast1.firebasedatabase.app",
    "projectId": "lawkey-561f0",
    "storageBucket": "lawkey-561f0.appspot.com",
    "messagingSenderId": "416592353192",
    "appId": "1:416592353192:web:177992bf2343da4edaaf9d"
}
#firebase_admin.initialize_app(creden)
firebase = pyrebase.initialize_app(config)
auther = firebase.auth()


def is_authenticated():
    return 'user' in st.session_state


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


# function to convert text to speech
def text_to_speech(text):
    tts = gTTS(text=text, lang='en')
    return tts


# function to play the speech
def play_speech(tts):
    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as temp_audio:
        tts.save(temp_audio.name)
        st.audio(temp_audio.name, format='audio/mp3')


# def login(email, password):
#     try:
#         auth_user = auth.sign_in_with_email_and_password(email, password)
#         return auth_user
#     except auth.InvalidEmailException:
#         return None
#     except auth.InvalidPasswordException:
#         return None
#     except auth.UserNotFoundException:
#         return None


def get_user_details(uid):
    try:
        user = auth.get_user(uid)
        st.write(user)
        return user
    except auther.AuthError as e:
        print("Error retrieving user details:", e)
        return None


# def signin():
#     signin_form = st.form(key='signin', clear_on_submit=True)
#     with signin_form:
#         email = st.text_input("Email")
#         password = st.text_input("Password", type="password")
#
#         if signin_form.form_submit_button("Login"):
#             try:
#                 st.write(email,password)
#                 user = auther.sign_in_with_email_and_password(email, password)
#                 st.success("Logged in successfully")
#                 st.write(user)
#             except Exception as e:
#
#                 st.write(e)
#                 st.error("Failed to log in")


def homepage():
    if 'signin_clicked' not in st.session_state:
        st.session_state.signin_clicked = False

    if not st.session_state.signin_clicked:
        bt1, bt2, bt3, bt4 = st.columns(4)
        if bt4.button('Already a Member?'):
            st.session_state.signin_clicked = True
    else:
        signin_form = st.form(key='signin', clear_on_submit=True)
        with signin_form:
            st.subheader('Sign In')
            email = st.text_input("Email")
            password = st.text_input("Password", type="password")

            if signin_form.form_submit_button("Login"):
                try:
                    user = auther.sign_in_with_email_and_password(email, password)
                    st.success("Logged in successfully")
                    st.session_state.user = user
                except Exception as e:
                    st.error("Failed to log in. Please try again.")
                    print("Error during login:", e)

    if not st.session_state.signin_clicked:
        signup_form = st.form(key='signup', clear_on_submit=True)
        with signup_form:
            st.subheader('Sign up')
            username = signup_form.text_input('User Name')
            email = signup_form.text_input('Email')
            password = signup_form.text_input('Password', type='password')
            confirm_password = signup_form.text_input('Confirm Password', type='password')
            if signup_form.form_submit_button('Sign Up'):
                if password == confirm_password:
                    try:
                        auth.create_user(email=email, password=password, uid=username)
                        st.success('Account created successfully')
                        st.session_state.signin_clicked = True  # Automatically switch to sign-in after sign-up
                    except Exception as e:
                        st.error('An error occurred during signup. Please try again.')
                        print("Error during signup:", e)
                else:
                    st.error('Passwords do not match')


def chatbot():
    st.title("LAW-Key")
    with st.sidebar:
        if st.button("Log Out"):
            logout()

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


def logout():
    # Clear session state to remove user authentication information
    if 'user' in st.session_state:
        del st.session_state['user']
    st.session_state.signin_clicked = False  # Reset signin_clicked flag if needed
    st.session_state.messages = []  # Clear chat history if needed
    # You can also clear any other session state variables that need to be reset upon logout

    # Sign out user from Firebase
    try:
        auth.revoke_refresh_tokens(st.session_state.user['idToken'])
    except Exception as e:
        print("Error during logout:", e)

    homepage()


def main():
    st.sidebar.title("Navigation")
    if is_authenticated():
        page_options = ["Chatbot", "Account", "About us", "Help"]
        selected_page = st.sidebar.selectbox("Select Page", page_options)

        if selected_page == "Chatbot":
            chatbot()
        elif selected_page == "Account":
            account()
        elif selected_page == "About us":
            about_us()
        elif selected_page == "Help":
            helpu()
    else:
        homepage()


if __name__ == "__main__":
    main()
