# LawKey---Law-Constitution-Chatbot

In response to the lack of legal awareness among Sri Lankans, this research introduces a law constitution chatbot with the help of Natural Language Processing (NLP) and Q-learning. This research introduces a law constitution chatbot leveraging Natural Language Processing (NLP) and Q-learning to address the lack of legal awareness among Sri Lankans. By utilizing the google-news-300 pre-trained word2vec model and TF-IDF to vectorize laws and queries, and employing cosine similarity for relevance assessment, the chatbot extracts relevant laws from the Sri Lankan constitution based on user input. Developed within the Rasa Framework, which employs NLU to discern user intents, the chatbot provides tailored legal guidance by offering summaries of the top three related laws. Integrating reinforcement learning, specifically Q-learning, enables the chatbot to refine its behavior through user feedback, ensuring optimal selection of relevant laws over time. Drawing upon successful applications in countries like Canada and India, this research aims to educate the general public on various legal domains in Sri Lanka. By creating a dataset from the Sri Lankan constitution and acts, and employing NLP techniques, including keyword extraction, this project contributes to advancing legal awareness in Sri Lanka. A comprehensive literature review underscores the potential of NLP and reinforcement learning techniques in legal chatbots, particularly highlighting the adaptability of Q-learning. Through a comprehensive analysis of legal chatbots, this project aims to foster a more informed society in Sri Lanka contributing to the theoretical foundation and practical implementation of legal guidance systems.

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
