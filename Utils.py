import pandas as pd
import random


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
    #     print(df)
    map_index2action, map_action2index = actions_to_dict(df)
    # print(map_index2action)
    map_index2state, map_state2index = state_to_dict(df)
    # print(map_index2state)

    mapping = {}
    mapping['index2action'] = map_index2action
    mapping['action2index'] = map_action2index
    mapping['index2state'] = map_index2state
    mapping['state2index'] = map_state2index

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


def get_mapping(df):
    """ return dictionary mapping set of states (utterances) to indices and viceversa, and set of actions (responses) to indices and viceversa """

    map_index2action, map_action2index = actions_to_dict(df)
    # print(map_index2action)
    map_index2state, map_state2index = state_to_dict(df)
    # print(map_index2state)

    mapping = {}
    mapping['index2action'] = map_index2action
    mapping['action2index'] = map_action2index
    mapping['index2state'] = map_index2state
    mapping['state2index'] = map_state2index

    return mapping


class Simulator(object):

    def __init__(self, conv_dict, multiply=4):
        """ initialize parent sample of conversation and random generator """

        self.conv_dict = conv_dict

        all_utt = list(conv_dict['utterance'])
        feedback = list(conv_dict['feedback'])

        ## define parent sample of conversations: self.utt such that extraction
        ## of utterance triggering resp  with negative feedback has higher probability
        ## probability ratio negative:positive defined by multiply
        wrongs = []
        good = []
        utt = []

        for i in range(len(all_utt)):
            if feedback[i] == 0:
                utt.append(all_utt[i])
            else:
                for k in range(multiply):
                    utt.append(all_utt[i])

        self.utt = utt
        self.N = len(self.utt)

        print()
        print('---------------------------------------------------------------------------')
        print('Parent sample of conversations in Simulator contains %d questions' % self.N)

        ## init random generator
        seed = 45896
        random.seed(seed)

        self.iterator = conv_dict.iterrows()

        return

    def run_random(self):
        """ Returns random action """

        r = random.randint(0, self.N - 1)
        return self.utt[r]

    def sequential(self, reset=False):
        """ return action in sequential order """

        if reset:
            self.iterator = None
            self.iterator = self.conv_dict.iterrows()
            print('resetting...', self.iterator)

        try:
            return next(self.iterator)[1]
        except StopIteration:
            return None