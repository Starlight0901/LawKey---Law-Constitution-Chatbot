import speech_recognition as sr
import PySimpleGUI as gui 

gui.theme('Darkblue')
gui.set_options(font=('Calibri',15))

Layout = [[gui.Text("Speech to text")],
          [gui.Multiline(size = (70,20),key="-OUTPUT-")],
          [gui.Button("Record",button_color=('white')),
           gui.Button("Stop Recording", button_color=('yellow')),
          gui.Button("End", button_color=('red'))]
]
window = gui.Window("Speech to Text",Layout)
listening = False
while True:
  event,values = window.read()
  if event== "End" or event == gui.WIN_CLOSED:
    break
  elif event == "Record":
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
     audio = recognizer.listen(source)
    try:
        text = recognizer.recognize_google(audio)
        window["-OUTPUT-"].update(text)
    except sr.UnknownValueError:
        window["-OUTPUT-"].update("could not understand")
    except sr.RequestError:
        window["-OUTPUT-"].update("Error with the service ".format(e))

  elif  event == "Stop Recording" and listening:
        listening = False 
        recognizer.energy_threshold = 1000  
        window["-OUTPUT-"].update("Stopped recording")
        continue
window.close()       

