import random
import re
import pandas as pd
from nltk.corpus import stopwords
import gensim.downloader as api
from q_table import Q_table
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer
import requests
from LawKey.actions.actions import law_cleaning, tokenize, remove_stopwords, stemmer

df = pd.read_csv("C:\\Users\\admin\\Desktop\\L5\\DSGP\\LawKey---Law-Constitution-Chatbot\\data.csv")
word_model = api.load("word2vec-google-news-300")
vectorized = TfidfVectorizer(stop_words=stopwords.words("english"))
doc_vectors_tfidf = vectorized.fit_transform(df["Law"])
law_vectors_word2vec = []
for law in df["Law"]:
    law_tokens = tokenize(law_cleaning(law))
    law_tokens = remove_stopwords(law_tokens)
    law_vector = np.mean([word_model[word] for word in law_tokens if word in word_model], axis=0)
    law_vectors_word2vec.append(law_vector)

def calculate_similarity_random_laws(input_text):
    # Preprocess input text
    cleaned_text = law_cleaning(input_text)
    tokens = tokenize(cleaned_text)
    tokens = remove_stopwords(tokens)
    processed_text = stemmer(tokens)

    # Calculate similarity using both TF-IDF and Word2Vec
    input_vector_tfidf = vectorized.transform([processed_text])
    similarities_tfidf = cosine_similarity(input_vector_tfidf, doc_vectors_tfidf)[0]

    input_vector_word2vec = np.mean([word_model[word] for word in tokens if word in word_model], axis=0)
    similarities_word2vec = cosine_similarity([input_vector_word2vec], law_vectors_word2vec)[0]

    # Combine similarities (example: simple average)
    combined_similarities = (similarities_tfidf + similarities_word2vec) / 2
    highest_similarity = max(combined_similarities)

    sorted_indices = np.argsort(combined_similarities)[::-1][:10]
    top_indices = sorted_indices[3:]
    laws = df["Law"].iloc[top_indices].tolist()

    random_laws = random.sample(laws, k=3)

    return highest_similarity , random_laws

def preprocess_response(response):
    # Convert to lowercase
    response = response.lower()
    # Remove leading and trailing whitespace
    response = response.strip()
    # Remove extra whitespace within the response
    response = re.sub(r'\s+', ' ', response)
    return response

class Agent:

    def __init__(self, mapping,q_tab):
        self.map_state2index = mapping['state2index']
        self.map_index2state = mapping['index2state']
        self.map_action2index = mapping['action2index']
        self.map_index2action = mapping['index2action']
        self.feedback = mapping['feedback']

        self.q_table = q_tab
        # self.states = states
        # self.actions = actions
        # self.learning_rate = learning_rate
        # self.discount_factor = discount_factor
        # self.exploration_rate = exploration_rate

    def select_action(self, most_similar_state, state):
        if most_similar_state is not None:
            q_values = self.q_table.get_q_values_for_state(most_similar_state)
            max_q_value_index = np.argmax(q_values)
            min_q_value_index = np.argmin(q_values)

            # Check if the maximum Q-value is greater than zero
            if max(q_values) > 0:
                action = self.map_index2action[max_q_value_index]
                # similarity, random_laws = calculate_similarity_random_laws(most_similar_state)
                print(action)
                print('first')
                print(max(q_values))
                return action , max(q_values)
            elif min(q_values) < 0:
                rasa_response = self.get_response_from_rasa(state)
                preprocessed_rasa_response = preprocess_response(rasa_response)
                preprocessed_q_table_action = preprocess_response(self.map_index2action[min_q_value_index])
                if preprocessed_rasa_response == preprocessed_q_table_action:
                    similarity, random_laws = calculate_similarity_random_laws(state)
                    message = f"Here are the top 3 relevant laws based on your query:\n\n"
                    for law in random_laws:
                        message += f"-> {law}\n"
                    print('second one')
                    print(message)
                    return message , 0
                else:
                    similarity, random_laws = calculate_similarity_random_laws(state)
                    print(min(q_values))
                    print('third one')
                    # print('q: ',preprocessed_q_table_action)
                    # print('rasa: ', preprocessed_rasa_response)
                    return rasa_response, similarity
            else:
                response = self.get_response_from_rasa(state)
                similarity, random_laws = calculate_similarity_random_laws(state)
                print('4 th one')
                return response , similarity
        else:
            response = self.get_response_from_rasa(state)
            similarity, random_laws = calculate_similarity_random_laws(state)
            print('last one')
            return response , similarity

    def get_response_from_rasa(self, state):
        rasa_server_url = "http://localhost:5005/webhooks/rest/webhook"
        response = requests.post(rasa_server_url, json={"message": state})

        rasa_response = response.json()

        if len(rasa_response) > 1:
            message = rasa_response[0]['text']
            laws = rasa_response[1]['text']

            # Split laws based on "-" sign and get the first 3 laws
            law_list = laws.split('-')
            first_3_laws = '\n'.join(law_list[:4])

            formatted_output = f"{message}\n{first_3_laws}"
            similarity, random_laws = calculate_similarity_random_laws(state)
            # print(formatted_output)
            print(similarity)
            return formatted_output
        elif len(rasa_response) == 1:
            message = rasa_response[0]['text']
            formatted_output = f"{state}\n{message}"
            print(formatted_output)
            return formatted_output
        else:
            return 0

# state = 'what are the civil laws'
#
# dispatcher = CollectingDispatcher()
# domain = {}
# response = RetrieveLaws().run(dispatcher, state, domain)
# print(response)
# tracker = Tracker
# response = test_retrieve_laws_action(tracker)
# print(response)









