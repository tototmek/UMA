import random
import json
import math


class QLearningAlgorythm:
    def __init__(self, possible_moves, gamma, beta, epsilon):
        self.Q = {}
        self.possible_moves = possible_moves
        self.gamma = gamma
        self.beta = beta
        self.epsilon = epsilon

    def change_epsilon(self, new_epsilon):
        self.epsilon = new_epsilon

    def make_Q(self, state):
        def make_temp_moves():
            temp = {}
            for move in self.possible_moves:
                temp[move] = 0
            return temp
        try:
            x = self.Q[state[0]]
        except KeyError as e:
            temp1 = {}
            temp2 = {}
            temp1[state[2]] = make_temp_moves()
            temp2[state[1]] = temp1
            self.Q[state[0]] = temp2
            return
        try:
            x = self.Q[state[0]][state[1]]
        except KeyError as e:
            temp1 = {}
            temp1[state[2]] = make_temp_moves()
            self.Q[state[0]][state[1]] = temp1
            return
        try:
            x = self.Q[state[0]][state[1]][state[2]]
        except KeyError as e:
            self.Q[state[0]][state[1]][state[2]] = make_temp_moves()
            return

    def make_move(self, state):
        if self.epsilon > 0:
            random_int = random.randint(0, 100)
            if random_int < self.epsilon:
                action = random.choice(self.possible_moves)
                return action
        return self.make_move_optimal(state)

    def make_move_optimal(self, state):
        q = self.Q[state[0]][state[1]][state[2]]
        best_action = [[], -math.inf]
        for action in q.keys():
            value = q[action]
            if value > best_action[1]:
                best_action[0].clear()
                best_action[0].append(action)
                best_action[1] = value
            elif value == best_action[1]:
                best_action[0].append(action)
        action = random.choice(best_action[0]) if len(
            best_action[0]) > 1 else best_action[0][0]
        return action

    def default_learning(self, next_state, is_terminated, state, action, reward):
        q_old_state = self.Q[state[0]][state[1]][state[2]]
        q_new_state = self.Q[next_state[0]][next_state[1]][next_state[2]]
        new_keys = list(q_new_state.keys())
        old_keys = q_old_state.keys()
        next_state_values = max([q_new_state[u]
                                 for u in new_keys]) if not is_terminated else 0

        if action in old_keys:
            self.Q[state[0]][state[1]][state[2]][action] += \
                self.beta * (reward + self.gamma *
                             next_state_values - q_old_state[action])

    def save_Q(self, file_name="sample.json"):
        json_object = json.dumps(self.Q, indent=4)

        with open(file_name, "w") as outfile:
            outfile.write(json_object)
