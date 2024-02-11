import pandas as pd
import numpy as np
import pickle
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords

# Download stopwords list (run once)
import nltk
nltk.download('stopwords')

# Function to preprocess text and remove stopwords
def preprocess(text):
    tokens = word_tokenize(text.lower())
    stop_words = set(stopwords.words('english'))
    tokens = [word for word in tokens if word.isalnum() and word not in stop_words]
    return tokens

def keyword_matching(query, mapping):
    query_tokens = preprocess(query)
    similarity_scores = {}

    # Iterate over each state in the mapping
    for state_index, state_text in mapping['index2state'].items():
        state_tokens = preprocess(state_text)
        intersection = len(set(query_tokens) & set(state_tokens))  # Calculate the number of keyword matches
        similarity_percentage = (intersection / len(query_tokens)) * 100  # Calculate similarity percentage
        similarity_scores[state_index] = similarity_percentage

    # Find the state with the highest similarity percentage
    most_similar_state = max(similarity_scores, key=similarity_scores.get)
    highest_similarity_percentage = similarity_scores[most_similar_state]

    return most_similar_state, highest_similarity_percentage


