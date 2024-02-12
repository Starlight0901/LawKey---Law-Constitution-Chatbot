from typing import Any, Text, Dict, List
from keras.losses import cosine_similarity
from rasa_sdk import Action, Tracker
from rasa_sdk.events import SlotSet
from rasa_sdk.executor import CollectingDispatcher
import pandas as pd
import nltk
import string
from nltk.corpus import stopwords
from gensim.models import KeyedVectors
from sklearn.metrics.pairwise import cosine_similarity


# Load Word2Vec model
model_path = r"C:\Users\msi\Documents\GitHub\LawKey---Law-Constitution-Chatbot\chatbot\word2vec-google-news-300.model"
model = KeyedVectors.load(model_path)

# Load laws dataset
df = pd.read_csv(r"C:\Users\msi\Documents\GitHub\LawKey---Law-Constitution-Chatbot\chatbot\data.csv")

firstCol = df[df.columns[0]]
df = df.drop(columns=df.columns[0])
df[firstCol.name] = firstCol

df.drop_duplicates(inplace=True)
df.dropna(inplace=True)


# Data preprocessing functions
def law_cleaning(law):
    law = law.translate(str.maketrans('', '', string.punctuation + '\r\n\t'))
    law = law.replace('ã', '')
    law = law.replace('Ã', '')
    law = ''.join([i for i in law if i.isalnum() or i.isspace()])
    return law


def tokenize(text):
    tokens = nltk.word_tokenize(text.lower())
    return tokens


def remove_stopwords(tokens):
    stop_words = set(stopwords.words("english"))
    filtered = []
    for token in tokens:
        if token.lower() not in stop_words:
            filtered.append(token)
    return filtered


def stemmer(tokens):
    pstemmer = nltk.PorterStemmer()
    stemmed_words = []
    for token in tokens:
        stemmed_word = pstemmer.stem(token)
        stemmed_words.append(stemmed_word)
    stemmed_text = ' '.join(stemmed_words)
    return stemmed_text


df["law_clean"] = df["Law"].apply(law_cleaning)
df["tokens"] = df["law_clean"].apply(tokenize)
df["tokens"] = df["tokens"].apply(remove_stopwords)
df["tokens"] = df["tokens"].apply(stemmer)
df["tokens_w"] = df["tokens"].apply(tokenize)


# Calculate vectors for tokens
def get_mean_vectors(features):
    tokens = []
    for token in features:
        if token in model:
            tokens.append(token)
    if len(tokens) >= 1:
        return model.get_vector(tokens).mean(axis=0)
    else:
        return []


df["Vectors"] = df["tokens_w"].apply(get_mean_vectors)


# Retrieve laws based on input text
def retrieve_laws(input_text):
    tokens = nltk.word_tokenize(input_text)
    tokens = [token for token in tokens if token.lower() not in stopwords.words('english')]
    tokens = [nltk.PorterStemmer().stem(word) for word in tokens]

    input_vectors = get_mean_vectors(tokens)
    similarity_level = cosine_similarity([input_vectors], df['Vectors'].tolist())[0]
    df['similarity_to_input'] = similarity_level

    related_laws = df.sort_values(by='similarity_to_input', ascending=False).head(1)['Law'].tolist()
    return related_laws


# Custom action class
class ActionRetrieveRelatedLaws(Action):
    def name(self) -> Text:
        return "action_retrieve_related_laws"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        input_text = tracker.latest_message.get("text")
        related_law = retrieve_laws(input_text)

        if related_law:
            response_message = f"The most related law is: {related_law[0]}"
            # Update the 'related_law' slot with the retrieved law
            return [SlotSet("related_law", related_law[0])]
        else:
            response_message = "Sorry, I couldn't find any related laws."

        dispatcher.utter_message(text=response_message)

        return []
