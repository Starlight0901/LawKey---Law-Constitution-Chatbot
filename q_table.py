from random import random

import numpy as np
import pickle

class Q_table(object):

    def __init__(self, mapping):
        self.map_state2index = mapping['state2index']
        self.map_index2state = mapping['index2state']
        self.map_action2index = mapping['action2index']
        self.map_index2action = mapping['index2action']
        self.feedback = mapping['feedback']

        self.learning_rate = 0.01
        self.epsilon = 0.2

        self.num_states = len(self.map_state2index)
        self.num_actions = len(self.map_action2index)
        self.num_feedbacks = len(self.feedback)
        print('Q table size [states, actions, feedbacks]:', self.num_states, self.num_actions)

        # Initialize Q-values matrix
        self.Q = np.zeros([self.num_states+1, self.num_actions+1])

    def add(self, feedback, utterance_index, response_index):
        self.Q[utterance_index, response_index] = feedback
        return

    def get_q_values_for_state(self, state_index):
        return self.Q[state_index, :]

    def update_q_value(self, state_index, action_index, new_value):
        self.Q[state_index, action_index] = new_value

    def save_q_table(self, q_table, filename = 'Q.pkl'):
        with open(filename, 'wb') as f:
            pickle.dump(q_table, f)

    # Load Q table from a file
    def load_q_table(self, filename = 'Q.pkl'):
        with open(filename, 'rb') as f:
            q_table = pickle.load(f)
        return q_table





