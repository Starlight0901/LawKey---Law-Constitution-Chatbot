# LawKey---Law-Constitution-Chatbot
LawKey - Law Constitution Chatbot

Explaination of Law-Key chatbot

## Steps to execute the application:

### Installing Libraries
Before you run the application check if the needed libraries are installed. If not execute the below pip install commands in your terminal to install the libraries.
- pip install firebase-admin
- pip install streamlit
- pip install SpeechRecognition
- pip install gTTS
- pip install pyrebase4
- pip install pyAudio
- pip install rasa
- pip install gensim
- pip install nltk

### Change Filepaths
Make sure to change the file paths in the below code lines of the files
actions.py - line 51, line 122
agent.py - line 14

### Execute the below commands in the terminal to run the application
In the 1st terminal, execute the below commands
1. cd LawKeyChatbot
2. rasa run actions

In another terminal, execute the below command
1. cd LawKeyChatbot
2. rasa shell

In another terminal, execute the below command
1. streamlit run LawKey1.py
