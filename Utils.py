import pandas as pd
import random
from q_table import Q_table
from agent import Agent


def parameters():
    config = {}
    config['log_file'] = ''
    config['epochs'] = 500
    config['learning_rate'] = 0.2
    config['l2_reg'] = 0.1
    config['num_episodes_warm'] = 100
    config['train_freq_warm'] = 100
    config['num_episodes'] = 100
    config['train_freq'] = 10
    config['epsilon'] = 0.2
    config['epsilon_f'] = 0.05
    config['epsilon_epoch_f'] = 20
    config['dqn_hidden_size'] = 60
    config['gamma'] = 0.9
    config['prob_no_intent'] = 0.5
    config['buffer_size'] = 10000
    return config


def filter_and_dropna(file_path):
    df = pd.read_csv(file_path)
    keep_words = ['what', 'which', 'when', 'where', 'who', 'whom', 'whose', 'why', 'whether', 'how', 'is', 'are']

    def starts_with_keep_words(sentence):
        return any(sentence.lower().lstrip().startswith(word) for word in keep_words)

    filtered_df = df[df['utterance'].astype(str).apply(starts_with_keep_words)]
    filtered_df.dropna(subset=['utterance'], inplace=True)

    return filtered_df


def load_data():
    file = 'GS_short_corrected.csv'
    df = pd.read_csv(file)

    df.dropna(subset=['utterance'], how='all', inplace=True)
    df.dropna(subset=['response'], how='all', inplace=True)
    df = filter_and_dropna(file)
    print(df)
    map_index2action, map_action2index = actions_to_dict(df)
    # print(map_index2action)
    map_index2state, map_state2index = state_to_dict(df)
    # print(map_index2state)
    feedback = df['feedback']


    mapping = get_mapping(df)
    q_tab = Q_table(mapping)
    populate_q_table(df,mapping,q_tab)

    mapping = {}
    mapping['index2action'] = map_index2action
    mapping['action2index'] = map_action2index
    mapping['index2state'] = map_index2state
    mapping['state2index'] = map_state2index
    mapping['feedback'] = feedback

    states = 'Where is Brillancourt'
    agent = Agent(mapping,q_tab)
    agent.select_action(states)

    return mapping , df


def state_to_dict(df):
    utterances = list(df['utterance'])

    unique_utterances = list(set(utterances))
    #     print('# utterances in final DF:', len(utterances), len(list(set(utterances))))

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


def get_mapping(df):


    map_index2action, map_action2index = actions_to_dict(df)
    # print(map_index2action)
    map_index2state, map_state2index = state_to_dict(df)
    # print(map_index2state)
    feedback = df['feedback']
    print(feedback)

    mapping = {}
    mapping['index2action'] = map_index2action
    mapping['action2index'] = map_action2index
    mapping['index2state'] = map_index2state
    mapping['state2index'] = map_state2index
    mapping['feedback'] = feedback

    return mapping


def populate_q_table(conv_dict, mapping, Q_tab):

    map_state2index = mapping['state2index']
    map_action2index = mapping['action2index']
    feedback = mapping['feedback']  # Retrieve the feedback Series

    # Print column headers for states and actions
    print('States:', list(map_state2index.keys()))
    print('Actions:', list(map_action2index.keys()))

    for index, row in conv_dict.iterrows():
        state_index = map_state2index[row['utterance']]
        print(state_index, map_state2index)
        action_index = map_action2index[row['response']]
        feedback_value = feedback[index]

        Q_tab.add(feedback_value, state_index, action_index)

    for state, row in zip(map_state2index.keys(), Q_tab.Q):
        print(state, ' '.join([str(int(value)) for value in row]))





load_data()


