from flask import Flask, render_template
import speech_recognition as sr

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('chatbot_interface.html')

@app.route('/voice', methods=['POST'])
def voice():
    recognizer = sr.Recognizer()
    text=''
    with sr.Microphone() as source:
        print("Speak")
        audio = recognizer.listen(source)
    try:
        text = recognizer.recognize_google(audio)
        print("You said: " + text)
    except sr.UnknownValueError:
        print("Could not understand")
    except sr.RequestError as e:
        print("Error with the service: " + str(e))
    return render_template('chatbot_interface.html',Text= text)
    
if __name__ == '__main__':
    app.run(debug=True)
