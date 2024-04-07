import tempfile
from datetime import datetime
from firebase_admin import auth
import streamlit as st
import speech_recognition as sr
from gtts import gTTS
import run
import pyrebase

# fire base configuration
config = {
    "apiKey": "AIzaSyDt4EqnrB2clEi1G2Mf_5OIyV9c2lfgE9M",
    "authDomain": "lawkey-561f0.firebaseapp.com",
    "databaseURL": "https://lawkey-561f0-default-rtdb.asia-southeast1.firebasedatabase.app",
    "projectId": "lawkey-561f0",
    "storageBucket": "lawkey-561f0.appspot.com",
    "messagingSenderId": "416592353192",
    "appId": "1:416592353192:web:177992bf2343da4edaaf9d"
}
# Initializing Firebase app using Pyrebase
firebase = pyrebase.initialize_app(config)
auther = firebase.auth()

# Access Firestore client
db = firebase.database()


def is_authenticated():
    return 'user' in st.session_state


# function to voice to text
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


def get_chat_history(username):
    user_ref = db.child("users_chat").child(username)
    chat_history = user_ref.child("chatHistory").get()
    return chat_history


def save_chat_message(bot, username, content_user, content_bot):
    chat_ref = db.child("users_chat").child(username).child("chatHistory")
    timestamp = str(datetime.now())  # Converting timestamp to string
    new_chat_ref = chat_ref.push({
        'bot ': bot,
        'recipientId': username,
        'content_user': content_user,
        'content_bot': content_bot,
        'timestamp': timestamp
    })


def save_user_data(uid, email, username):
    user_data = {"email": email, "name": username}
    db.child("users_data").child(uid).set(user_data)


def get_user_details(uid):
    user_data = db.child("users_data").child(uid).get().val()
    user_name = user_data.get("name")
    return user_name


def homepage():
    if 'signin_clicked' not in st.session_state:
        st.session_state.signin_clicked = False

    if not st.session_state.signin_clicked:
        bt1, bt2, bt3, bt4 = st.columns(4)
        if bt4.button('Already a Member?'):
            st.session_state.signin_clicked = True
    else:
        if st.button('Create Account'):
            st.session_state.signin_clicked = False
        signin_form = st.form(key='signin', clear_on_submit=True) #sign in
        with signin_form:
            st.subheader('Sign In')
            email = st.text_input("Email")
            password = st.text_input("Password", type="password")

            if signin_form.form_submit_button("Login"):
                try:
                    user = auther.sign_in_with_email_and_password(email, password)
                    st.success("Sign in successfully")
                    user_name = get_user_details(user['localId'])
                    st.session_state.user = user_name

                except Exception as e:
                    st.error("Failed to sign in. Please try again.")
                    print("Error during login:", e)

    if not st.session_state.signin_clicked: #sign up
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
                        user = auther.create_user_with_email_and_password(email=email, password=password)
                        st.success('Account created successfully. You can now sign in using Already a member.')
                        uid = user['localId']
                        if uid:
                            # Save user data to database
                            save_user_data(uid, email, username)
                        st.session_state.signin_clicked = True  # Automatically switching to sign-in after sign-up
                        main()
                    except Exception as e:
                        st.error('An error occurred during signup. Please try again.')
                        print("Error during signup:", e)
                        return None
                else:
                    st.error('Passwords do not match')


def chatbot():
    st.title("LAW-Key")
    with st.sidebar:
        if st.button("Sign Out"):
            logout()

    recognized_text = st.chat_input("Say something")
    button_pressed = False
    col1, col2 = st.columns(2)
    if col1.button("🎙️ voice "):
        transcription = recognize_speech()
        recognized_text = transcription

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
            response, similarity, mapping, similar_state, q_table, query = run.main(recognized_text) #getting the responce
            st.session_state.session_data.append(
                {'query': query, 'similar_state': similar_state, 'response': response, 'similarity': similarity,
                 'mapping': mapping, 'q_table': q_table})  #saving the responce
            st.session_state.messages.append({"role": "AI", "content": response})
            save_chat_message("AI", st.session_state.user, query, response)
            st.session_state.voice = response
    if not st.session_state.messages:
        with st.chat_message("ai"):
            st.write("Hello ", st.session_state.user, "👋")
    else:
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])   #getting feedback for  R learning
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


def Chat_History():
    st.title("Chat History Viewer")
    chat_history = db.child("users_chat").child(st.session_state.user).child("chatHistory").get().val()

    if chat_history:
        st.subheader("Chat History")
        for message_key, message_data in chat_history.items():
            st.write("Timestamp:", message_data["timestamp"])
            st.write("Question:", message_data["content_user"])
            st.write("Answer:", message_data["content_bot"])
            st.write("---")
    else:
        st.write("No chat history available.")


def helpu():
    st.title("How can we Help")


def about_us():
    st.title("Welcome to LAW-Key ")
    st.subheader("Law Constitution Chatbot, ")
    st.write("where we fuse legal empowerment with technological innovation. Our Law Constitutional Chatbot app is "
             "tailored for Sri Lanka's intricate legal terrain, offering accessible and reliable guidance on various "
             "legal issues.")

    st.write("""
    -Specializing in
      Motor Traffic Laws
      Criminal Laws pertaining to the rights and entitlements of victims of crime and witnesses
      Procedural Civil Laws
      Labor Laws concerning wages
        
    our application offers unparalleled support to individuals navigating the intricacies of the Sri Lankan legal system by the law and explaination.
    """)

    st.write("Driven by a passion for democratizing legal knowledge, our team of experts has painstakingly curated a "
             "wealth of accurate and up-to-date information, ensuring that our users are equipped with the resources "
             "they need to make informed decisions.")


def logout():
    # Clear session state to remove user authentication information
    if 'user' in st.session_state:
        del st.session_state['user']
    st.session_state.signin_clicked = False
    st.session_state.messages = []  # Clearing chat history

    try:
        auth.revoke_refresh_tokens(st.session_state.user['idToken'])
    except Exception as e:
        print("Error during logout:", e)

    homepage()


def main():
    st.sidebar.title("Navigation")
    if is_authenticated():
        page_options = ["Chatbot", "Chat History", "About us"]
        selected_page = st.sidebar.selectbox("Select Page", page_options)

        if selected_page == "Chatbot":
            chatbot()
        elif selected_page == "Chat History":
            Chat_History()
        elif selected_page == "About us":
            about_us()
    else:
        homepage()


if __name__ == "__main__":
    main()
