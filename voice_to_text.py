import speech_recognition as sr
recognizer = sr.Recognizer()
with sr.Microphone() as source:
    print ("speak")
    audio = recognizer.listen(source)
try:
    text = recognizer.recognize_google(audio)
    print("you said   :"+text)
except sr.UnknownValueError:
    print("could not understand")
except sr.RequestError:
    print("Error with the service ".format(e))

    
