# The environment class creates an environment of Nodes (see Node.py). Each node is "told" the node in front
# and behind it (unless it is the starting or ending node). Nodes are dynamically created based on the constructor
# argument. These nodes are held in a list of nodes. The environment is capable of tracking the performance
# of the agent.

from Node import Node
import csv


class Environment(object):
    # Empty list of nodes to be populated.
    nodes = []

    # Constructor that instantiates nodes based on num_of_states
    # argument. The prev and next of each node is determined here.
    # Reward is added to the final node in the environment.
    def __init__(self, num_of_states):
        nodes = self.nodes
        for state_num in range(num_of_states):
            nodes.append(Node(state_num))
        for node in nodes:
            if node.state == 0:
                node.set_next(nodes[1])
            elif node.state == num_of_states - 1:
                node.prev == nodes[num_of_states - 2]
                node.add_reward()
            else:
                node.set_prev(nodes[node.state - 1])
                node.set_next(nodes[node.state + 1])