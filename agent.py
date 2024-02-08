from q_table import Q_table
import numpy as np
import pandas as pd

class Agent:

    def __init__(self, mapping):
        self.map_state2index = mapping['state2index']
        self.map_index2state = mapping['index2state']
        self.map_action2index = mapping['action2index']
        self.map_index2action = mapping['index2action']
        self.feedback = mapping['feedback']

        self.q_table = Q_table(mapping)
        # self.states = states
        # self.actions = actions
        # self.learning_rate = learning_rate
        # self.discount_factor = discount_factor
        # self.exploration_rate = exploration_rate

    def select_action(self, state):

        # Get the index of the state from map_state2index
        state_index = self.map_state2index[state]
        print(state_index)


            # Get the Q-values for the given state
        q_values = self.q_table.get_q_values_for_state(state_index)
        max_q_value_index = np.argmax(q_values)
        action = self.map_index2action[max_q_value_index]

        return action
        # except KeyError:
        #     print(f"State '{state}' not found in the mapping.")
        #     return None









