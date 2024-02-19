import numpy as np
import gensim.downloader as api
from rasa_sdk import Action
import pandas as pd
from rasa_sdk.events import SlotSet
from nltk.corpus import stopwords
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer

from utils.nlpUtils import tokenize, law_cleaning, remove_stopwords, stemmer
from utils.simplifedLawUtils import simplify_laws
from utils.summarizedLawUtils import summarize_laws_with_t5

# Load pre-trained word2vec model
word_model = api.load("word2vec-google-news-300")

# Load your law dataset (modify for your data path)
df = pd.read_csv("C:/Users/msi/Desktop/dsgp/data.csv")

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

        # Combine similarities (simple average)
        combined_similarities = (similarities_tfidf + similarities_word2vec) / 2

        # Retrieve top 3 relevant laws based on combined scores
        sorted_indices = np.argsort(combined_similarities)[::-1][:3]
        top_laws = df["Law"].iloc[sorted_indices].tolist()

        # Create and dispatch Rasa response
        message = f"Here are the top 3 relevant laws based on your query:\n\n"
        for law in top_laws:
            message += f"- {law}\n"
        dispatcher.utter_message(text=message)
        # Set the value of the retrieved_laws slot
        return [SlotSet("retrieved_laws", top_laws)]


class RetrieveSimplifiedLaws(Action):
    def name(self):
        return "retrieve_simplified_laws"

    def run(self, dispatcher, tracker, domain):
        retrieved_laws = tracker.get_slot("retrieved_laws")
        simplified_laws = simplify_laws(retrieved_laws)

        message = f"Here are the simplified versions of the retrieved laws:\n\n"
        for law in simplified_laws:
            message += f"- {law}\n"
        dispatcher.utter_message(text=message)

        return []


class RetrieveSummarizeLaws(Action):
    def name(self):
        return "retrieve_summarize_laws"

    def run(self, dispatcher, tracker, domain):
        retrieved_laws = tracker.get_slot("retrieved_laws")
        summarized_laws = summarize_laws_with_t5(retrieved_laws)

        message = f"Here are the summaries of the retrieved laws:\n\n"
        for law, summary in summarized_laws.items():
            message += f"**Law:** {law}\n**Summary:** {summary}\n\n"
        dispatcher.utter_message(text=message)

        return []


class RetrieveDescriptiveLaws(Action):
    def name(self):
        return "retrieve_descriptive_laws"

    def run(self, dispatcher, tracker, domain):
        retrieved_laws = tracker.get_slot("retrieved_laws")
        summarized_laws = summarize_laws_with_t5(retrieved_laws)

        # Combine summary and simplified version
        descriptive_laws = {}
        for law, summary in summarized_laws.items():
            simplified_law = simplify_laws(summary)
            descriptive_laws[law] = f"{simplified_law}\n(Summary: {summary})"

        message = f"Here are the descriptive summaries of the retrieved laws:\n\n"
        for law, description in descriptive_laws.items():
            message += f"**{law}**\n{description}\n\n"
        dispatcher.utter_message(text=message)

        return []
