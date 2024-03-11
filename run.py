import pickle

import LawKey1
from agent import Agent
from Utils import load_data , populate_q_table
from q_table import Q_table
from embedding import keyword_matching
import csv


def save_mapping(mapping, filename = 'mapping.pkl'):
    with open(filename, 'wb') as f:
        pickle.dump(mapping, f)


# Load mapping from a file
def load_mapping(filename = 'mapping.pkl'):
    with open(filename, 'rb') as f:
        mapping = pickle.load(f)
    return mapping


def main(query):
    try:
        mapping, df  = load_data()
        q_table = Q_table(mapping)
        print("Attempting to load Q-table from file...")
        print(query)
        q_table.load_q_table()
        print("Q-table loaded successfully.")
        print("populating")
        populate_q_table(df,mapping,q_table)
        print("populate done")
        agent = Agent(mapping, q_table)
        similar_state, score = keyword_matching(query, mapping)
        response, similarity = agent.select_action(similar_state, query)
        q_table.save_q_table(q_table)
        print(response)
        return response,similarity , mapping,similar_state, q_table, query

    except Exception as e:
        print("An error occurred:", e)
        raise

def save(query,similar_state,response,feedback,similarity,mapping,q_table):
    fieldnames = ['utterance', 'response', 'feedback', 'confidence']

    # Write column names to CSV file if the file doesn't exist
    try:
        with open('query_responses.csv', 'x', newline='') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
    except FileExistsError:
        pass
    if similar_state is not None:
        if similarity > 0:
            map_action2index = mapping.get('action2index')  # Use .get() to safely access the dictionary
            if map_action2index is not None and response in map_action2index:
                action_index = map_action2index[response]
                q_value = similarity + feedback
                q_table.update_q_value(similar_state, action_index, q_value)

    with open('query_responses.csv', 'a', encoding='utf-8', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writerow({
            'utterance': query,
            'response': response,
            'feedback': feedback,
            'confidence': similarity
        })


if __name__ == "__main__":
    while True:
        try:
            query = input("Enter recognized text: ")

            response, similarity, mapping, similar_state, q_table, query = main(query)
            feedback = 0
            save(query, similar_state, response, feedback, similarity, mapping, q_table)
        except KeyboardInterrupt:
            print("\nTerminating the program.")
            break
        except Exception as e:
            print(f"An error occurred: {e}")
            raise

# def main(query):
#     try:
#         mapping, df = load_data()
#         q_tab = Q_table(mapping)
#         agent = Agent(mapping, q_tab)
#         similar_state, score = keyword_matching(query, mapping)
#         response = agent.select_action(similar_state, query)
#         return response
#     except Exception as e:
#         print("An error occurred:", e)
#         return None

