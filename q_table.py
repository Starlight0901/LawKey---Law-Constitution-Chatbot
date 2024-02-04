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
        print('Q table size [states, actions, feedbacks]:', self.num_states, self.num_actions, self.num_feedbacks)

        # Initialize Q-values matrix
        self.Q = np.zeros([self.num_states, self.num_actions])

    def add(self, feedback, utterance_index, response_index):
        self.Q[utterance_index, response_index] = feedback
        return



    def get_q_value(self, state_index, action_index, feedback_index):
        return self.Q[state_index, action_index, feedback_index]

    def update_q_value(self, state_index, action_index, feedback_index, new_value):
        self.Q[state_index, action_index, feedback_index] = new_value

    def predict(self, i_s):

        Q_row = self.Q[i_s, :]

        return np.argmax(Q_row), np.amax(Q_row)

    def save_Q(self, pfile = 'Q.pck'):

        with open(pfile, 'wb') as f:
            pickle.dump(self.Q, f)

        return

    def load_Q(self, pfile='Q.pck'):

        with open(pfile, 'rb') as f:
            self.Q = pickle.load(f)

        return

    def learn(self, index_state, index_action, reward):

        current_q = self.Q[index_state, index_action]
        # using Bellman Optimality Equation to update q function
        new_q = float(reward)

        self.Q[index_state, index_action] += self.learning_rate * (new_q - current_q)

        return



