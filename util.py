"""
Author(s):  1. Hanzala B. Rehan
            2. Amna Akhtar Nawabi
            3. Abdullah Janjua
Description: This script defines several classes used for search algorithms in pathfinding or puzzle-solving problems.
             It includes `Node` to represent states in the search tree, `StackFrontier` for Depth-First Search (DFS),
             `QueueFrontier` for Breadth-First Search (BFS), and `PriorityQueueFrontier` for informed searches like A*.
Date created: November 15th, 2024
Date last modified: November 18th, 2024
"""


class Node:
    def __init__(self, state, parent, action):
        """
        Desc: Initializes a node for the search tree.
        Parameters:
            state (tuple): The current state (position) of the node.
            parent (Node): The parent node that led to this node.
            action (str): The action taken to reach this node from the parent.
        """
        self.state = state  # The current state as (row, col)
        self.parent = parent  # Parent node
        self.action = action  # Action taken to reach this node


class CostNode:
    def __init__(self, state, parent, action, cost):
        """
        Desc: Initializes a node for the search tree.
        Parameters:
            state (tuple): The current state (position) of the node.
            parent (Node): The parent node that led to this node.
            action (str): The action taken to reach this node from the parent.
            cost (int): The cost required to reach this node
        """
        self.state = state  # The current state as (row, col)
        self.parent = parent  # Parent node
        self.action = action  # Action taken to reach this node
        self.cost = cost  # Cost required to reach this node


class StackFrontier:
    def __init__(self):
        """
        Desc: Initializes an empty stack-based frontier.
        """
        self.frontier = []  # List to store nodes in the frontier

    def add(self, node):
        """
        Desc: Adds a node to the frontier.
        Parameters:
            node (Node): The node to be added.
        """
        self.frontier.append(node)

    def contains_state(self, state):
        """
        Desc: Checks if a state is already in the frontier.
        Parameters:
            state (tuple): The state to check.
        returns:
        (bool): True if state is in the frontier, False otherwise.
        """
        return any(node.state == state for node in self.frontier)

    def empty(self):
        """
        Desc: Checks if the frontier is empty.
        returns:
        (bool): True if frontier is empty, False otherwise.
        """
        return len(self.frontier) == 0

    def remove(self):
        """
        Desc: Removes and returns the last node added (LIFO).
        returns:
        (Node): The last node in the frontier.
        raises:
        Exception: If the frontier is empty.
        """
        if self.empty():
            raise Exception("empty frontier")
        else:
            node = self.frontier[-1]  # Get the last node
            self.frontier = self.frontier[:-1]  # Remove the last node
            return node


class QueueFrontier(StackFrontier):
    def remove(self):
        """
        Desc: Removes and returns the first node added (FIFO).
        returns:
        (Node): The first node in the frontier.
        raises:
        Exception: If the frontier is empty.
        """
        if self.empty():
            raise Exception("empty frontier")
        else:
            node = self.frontier[0]  # Get the first node
            self.frontier = self.frontier[1:]  # Remove the first node
            return node


class PriorityQueueFrontier(QueueFrontier):
    def __init__(self, func, goal):
        """
        Desc: Initializes a priority queue frontier.
        Parameters:
            func (function): A function to determine the priority of nodes.
        """
        super().__init__()  # Initialize the frontier as an empty list
        self.func = func  # Function to calculate priority
        self.goal = goal  # Goal of the maze

    def add(self, node):
        """
        Desc: Adds a node to the frontier and sorts it based on priority.
        Parameters:
            node (Node): The node to be added.
        """
        self.frontier.append(node)  # Add node to the frontier
        self.frontier.sort(key=lambda n: self.func(n, self.goal))  # Sort the frontier based on the priority function


def manhattan_distance(node, goal):
    """
    Desc: Returns the manhattan distance from a node to goal.
    Parameters:
        node (Node): Node to check for distance to goal.
        goal (tuple): State at which the goal exists
    returns:
    (int): Manhattan distance.
    """
    dist = abs(node.state[0] - goal[0]) + abs(node.state[1] - goal[1])
    return dist


def cumulative_cost_function(node, goal):
    """
    Desc: Returns the manhattan distance + the cost from start from a node to goal.
    Parameters:
        node (CostNode): Node to check for distance to goal.
        goal (tuple): State at which the goal exists
    returns:
    (int): Manhattan distance + cost from start.
    """
    cost = manhattan_distance(node, goal) + node.cost
    return cost
