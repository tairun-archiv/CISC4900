# The ExpectedSarsaAgent relies on  Expected Sarsa to obtain a reward. The agent either randomly explores the environment
# or chooses the best action from experience. The agent gains experience from randomly exploring, so at first it will
# wander aimlessly until it randomly comes across the reward.

# Numpy is required as the q_table is a matrix. Random is also required for the RNG.
import numpy as np
import random
from LearningAgent import LearningAgent


class ExpectedSarsaAgent(LearningAgent):

    # TODO: Figure out why ExpectedSarsaAgent requires this to work.
    def __init__(self):
        self.actions = []
        self.q_table = {}

    # If the current state hasn't been experienced yet, add it and create a 0 column for it.
    # If the current state has been experienced, return the state and action value.
    def q(self, state, action=None):
        if state not in self.q_table:
            self.q_table[state] = np.zeros(len(self.actions))
        if action is None:
            return self.q_table[state]
        return self.q_table[state][action]

    # If the RNG rolls less than epsilon, randomly choose an action based on available actions.
    # Otherwise, choose an action based on experience (refer to q_table).
    def choose_action(self, state):
        if random.uniform(0, 1) < self.epsilon:
            action = random.choice(self.actions)
            # print("RNG rolled " + str(action) + ".", end="", flush=True)
            return action
        else:
            action = np.argmax(self.q(state))
            #  print("Best action from experience is " + str(action) + ".", end="", flush=True)
            return action

    # See Agent.py
    def traverse(self, environment, index, csv_writer):
        print("Expected Sarsa Agent:")
        # Initialize possible actions based on environment size.
        for node in environment.nodes:
            self.actions.append(node.state)
        time = 0

        # Based on current state and action, decide where to go next, if the agent has reached a terminal state,
        # and what reward is obtained.
        def act(state, action):
            # If action is 1, the agent can progress to the next state.
            if action == 1:
                state = state.next
                print("Agent moved to node " + str(state.state))
                terminal_state = False
                reward = 0
            # Else, the agent is returned to the starting state of the environment.
            else:
                reward = 0
                state = environment.starting_node
                print("Agent moved to starting state.")
                terminal_state = False
            # If current state has a reward, give reward.
            if state.reward is True:
                reward = 100
                terminal_state = True
            return state, reward, terminal_state

        # For each episode, the initial state is the starting state in the environment,
        # the reward is zero'd, the alpha chosen corresponds to the number of the episode.
        for episode in range(self.number_of_episodes):
            state = environment.starting_node
            total_reward = 0
            alpha = self.decaying_alphas[episode]
            # For each step, it chooses a new action, determines the next state, reward, and if the next state is
            # terminal or not. Then the Sarsa function is calculated and the agent moves to the next state.
            for step in range(self.number_of_steps):
                time = time + 1
                action = self.choose_action(state)
                next_state, reward, terminal_state = act(state, action)
                total_reward += reward
                best_action = np.argmax(self.q(next_state))
                expected_return = (
                        (1 - self.epsilon) * self.q(next_state, best_action) + (self.epsilon / len(self.actions))
                        * sum(self.q(next_state, act) for act in range(len(self.actions))))
                self.q(state)[action] = self.q(state, action) + alpha * (
                        reward + self.gamma * expected_return - self.q(state, action))
                state = next_state
                self.write_to_csv(csv_writer, episode + 1, state, total_reward, time, action, index)
                if terminal_state:
                    print("Agent obtained reward.")
                    break
            print("Episode " + str(episode + 1) + ": " + "Reward = " + str(total_reward))
            print("Steps taken: " + str(step + 1) + "\n")
