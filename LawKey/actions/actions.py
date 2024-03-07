from rasa_sdk import Action
import numpy as np
import pandas as pd
import gensim.downloader as api
from nltk.corpus import stopwords
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer
<<<<<<< HEAD

from utils.utils import law_cleaning, tokenize, remove_stopwords, stemmer
=======
import nltk
import string
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer


nltk.download('punkt')
nltk.download('stopwords')


def law_cleaning(law):
    # Remove punctuations
    law = law.translate(str.maketrans('', '', string.punctuation + '\r\n\t'))

    # Remove special characters
    law = law.replace('ã', '')
    law = law.replace('Ã', '')

    # Remain only the alphabetic, numeric characters and whitespaces
    law = ''.join([i for i in law if i.isalnum() or i.isspace()])
    return law


def tokenize(text):
    tokens = nltk.word_tokenize(text.lower())
    return tokens


def remove_stopwords(tokens):
    stop_words = set(stopwords.words("english"))
    filtered = [token for token in tokens if token.lower() not in stop_words]
    return filtered


def stemmer(tokens):
    # Create the Porter stemmer object
    pstemmer = PorterStemmer()
    stemmed_words = [pstemmer.stem(token) for token in tokens]
    # Join the list of stemmed words into a single string separated by spaces
    stemmed_text = ' '.join(stemmed_words)
    return stemmed_text
>>>>>>> Reinforcement-learning

# Load pre-trained word2vec model
word_model = api.load("word2vec-google-news-300")

# Load your law dataset (modify for your data path)
<<<<<<< HEAD
df = pd.read_csv("C:/Users/msi/Desktop/dsgp/data.csv")
=======
df = pd.read_csv("C:\\Users\\asus\\OneDrive\\Desktop\\DSGP\\LawKey---Law-Constitution-Chatbot\\LawKey\\actions\\data.csv")
>>>>>>> Reinforcement-learning

# Preprocess data for efficiency
vectorized = TfidfVectorizer(stop_words=stopwords.words("english"))
doc_vectors_tfidf = vectorized.fit_transform(df["Law"])

law_vectors_word2vec = []
for law in df["Law"]:
    law_tokens = tokenize(law_cleaning(law))
    law_tokens = remove_stopwords(law_tokens)
    law_vector = np.mean([word_model[word] for word in law_tokens if word in word_model], axis=0)
    law_vectors_word2vec.append(law_vector)


class RetrieveLaws(Action):
    def name(self):
        return "retrieve_laws"

    def run(self, dispatcher, tracker, domain):
        user_text = tracker.latest_message.get("text")

        # Preprocess user input using functions from utils.py
        cleaned_text = law_cleaning(user_text)
        tokens = tokenize(cleaned_text)
        tokens = remove_stopwords(tokens)
        processed_text = stemmer(tokens)

        # Calculate similarity using both TF-IDF and Word2Vec
        input_vector_tfidf = vectorized.transform([processed_text])
        similarities_tfidf = cosine_similarity(input_vector_tfidf, doc_vectors_tfidf)[0]

        input_vector_word2vec = np.mean([word_model[word] for word in tokens if word in word_model], axis=0)
        similarities_word2vec = cosine_similarity([input_vector_word2vec], law_vectors_word2vec)[0]

<<<<<<< HEAD
        # Combine similarities (simple average)
=======
        # Combine similarities (example: simple average)
>>>>>>> Reinforcement-learning
        combined_similarities = (similarities_tfidf + similarities_word2vec) / 2

        # Retrieve top 3 relevant laws based on combined scores
        sorted_indices = np.argsort(combined_similarities)[::-1][:3]
        top_laws = df["Law"].iloc[sorted_indices].tolist()

        # Create and dispatch Rasa response
        message = f"Here are the top 3 relevant laws based on your query:\n\n"
        for law in top_laws:
            message += f"- {law}\n"
        dispatcher.utter_message(text=message)

        return []
