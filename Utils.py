import pandas as pd
import random
from q_table import Q_table
from agent import Agent
from embedding import keyword_matching


def parameters():
    config = {}
    config['learning_rate'] = 0.2
    config['epsilon'] = 0.2
    config['epsilon_f'] = 0.05
    config['epsilon_epoch_f'] = 20
    return config


def filter_and_dropna(file_path):
    df = pd.read_csv(file_path)
    keep_words = ['what', 'which', 'when', 'where', 'who', 'whom', 'whose', 'why', 'whether', 'how', 'is', 'are','do','can']

    def starts_with_keep_words(sentence):
        return any(sentence.lower().lstrip().startswith(word) for word in keep_words)

    filtered_df = df[df['utterance'].astype(str).apply(starts_with_keep_words)]
    filtered_df.dropna(subset=['utterance'], inplace=True)

    return filtered_df


def load_data():
    file = 'query_responses.csv'
    df = filter_and_dropna(file)

    df.dropna(subset=['utterance'], how='all', inplace=True)
    df.dropna(subset=['response'], how='all', inplace=True)
    #print(df)
    map_index2action, map_action2index = actions_to_dict(df)
    # print(map_index2action)
    map_index2state, map_state2index = state_to_dict(df)
    # print(map_index2state)
    feedback = df['feedback']
    similarity = df['confidence']

    mapping = {}
    mapping['index2action'] = map_index2action
    mapping['action2index'] = map_action2index
    mapping['index2state'] = map_index2state
    mapping['state2index'] = map_state2index
    mapping['feedback'] = feedback
    mapping['confidence'] = similarity

    # similar_state, score = embedding.keyword_matching(query, mapping)
    # print(similar_state)

    return mapping,df


def state_to_dict(df):
    utterances = list(df['utterance'])

    unique_utterances = list(set(utterances))

    count = 0
    map_index2state = {}
    map_state2index = {}

    for utt in unique_utterances:
        map_index2state[count] = utt
        map_state2index[utt] = count

        count += 1
    return map_index2state, map_state2index


def actions_to_dict(df):
    response = list(df['response'])
    #     print(response)
    unique_responces = list(set(response))
    #     print('# response in final DF:', len(response), len(list(set(response))))

    count = 0
    map_index2action = {}
    map_action2index = {}

    for resp in unique_responces:
        map_index2action[count] = resp
        map_action2index[resp] = count

        count += 1

    return map_index2action, map_action2index


def feedback_to_dict(df):
    feedbacks = list(df['feedback'])

    count = 0
    map_index2feedback = {}
    map_feedback2index = {}

    for utt in feedbacks:
        map_index2feedback[count] = utt
        map_feedback2index[utt] = count

        count += 1
    return map_index2feedback, map_feedback2index


def get_mapping(df,q_table):
    try:
        new_states, new_actions = {}, {}
        for index, row in df.iterrows():
            state = row['utterance']
            action = row['response']
            if state not in q_table:
                if state not in new_states:
                    new_states[state] = len(new_states)
                if action not in new_actions:
                    new_actions[action] = len(new_actions)
        map_index2action, map_action2index = actions_to_dict(df)
        map_index2state, map_state2index = state_to_dict(df)
        feedback = df['feedback']
        similarity = df['confidence']

        # Merge new states and actions into existing mapping
        mapping = {}
        mapping['index2action'] = {**map_index2action, **new_actions}
        mapping['action2index'] = {**map_action2index, **{v: k for k, v in new_actions.items()}}
        mapping['index2state'] = {**map_index2state, **new_states}
        mapping['state2index'] = {**map_state2index, **{v: k for k, v in new_states.items()}}
        mapping['feedback'] = feedback
        mapping['confidence'] = similarity


        return mapping
    except TypeError as e:
        print("An error occurred while creating the mapping:", e)
        return None


def populate_q_table(conv_dict, mapping, Q_tab):

    map_state2index = mapping['state2index']
    map_action2index = mapping['action2index']
    feedback = mapping['feedback']
    confidence_values = mapping['confidence']

    # print('States:', list(map_state2index.keys()))
    # print('Actions:', list(map_action2index.keys()))

    for index, row in conv_dict.iterrows():
        state_index = map_state2index[row['utterance']]
        #print(state_index, map_state2index)
        action_index = map_action2index[row['response']]
        feedback_value = feedback[index]
        confidence_value = confidence_values[index]

        new_q_value = feedback_value + confidence_value

        Q_tab.add(new_q_value, state_index, action_index)


    # for state, row in zip(map_state2index.keys(), Q_tab.Q):
    #     print(state, ' '.join([str(int(value)) for value in row]))


# load_data()
