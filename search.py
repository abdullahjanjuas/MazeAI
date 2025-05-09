"""
Author(s):  1. Hanzala B. Rehan
            2. Amna Akhtar Nawabi
            3. Abdullah Janjua
Description: Uses BFS, DFS, Greedy and A* Search.
Date created: November 18th, 2024
Date last modified: November 22nd, 2024
"""

from util import Node, CostNode, StackFrontier, QueueFrontier, PriorityQueueFrontier, manhattan_distance,\
    cumulative_cost_function
from maze import Maze


def breadth_first_search(start, maze):
    """
    Desc: Implements Breadth-First Search (BFS) to find the shortest path in an unweighted maze.
    Parameters:
        start (tuple): The starting position as (row, col).
        maze (Maze): An instance of the Maze class.
    returns:
        (list): A list of actions leading from the start to the goal, guaranteed to be the shortest path.
                 AND. A list of all the explored states.
    """

    start = Node(state=start, parent=None, action=None)
    frontier = QueueFrontier()
    frontier.add(start)

    # Explored set
    explored_states = set()
    explored = list()

    # Finding Solution:
    while True:

        if frontier.empty():
            raise Exception("No solution")

        node = frontier.remove()

        if node.state == maze.get_goal():
            path = []
            while node.parent is not None:
                path_element = tuple([node.action, node.state])
                path.append(path_element)
                node = node.parent
            path.reverse()
            return path[:-1], explored[1:]

        explored_states.add(node.state)
        explored.append(node.state)

        for action, state in maze.get_next(node):
            if not frontier.contains_state(state) and state not in explored_states:
                child = Node(state=state, parent=node, action=action)
                frontier.add(child)


def depth_first_search(start, maze):
    """
    Desc: Implements Depth-First Search (DFS) to find a path in the maze.
          While DFS may not always find the shortest path, it explores deeper nodes first.
    Parameters:
        start (tuple): The starting position as (row, col).
        maze (Maze): An instance of the Maze class.
    returns:
        (tuple): A list of actions leading from the start to the goal, guaranteed to be the shortest path.
                 AND. A list of all the explored states.
    """
    start = Node(state=start, parent=None, action=None)
    frontier = StackFrontier()
    frontier.add(start)

    # Explored set
    explored_states = set()
    explored = list()

    # Finding Solution:
    while True:

        if frontier.empty():
            raise Exception("No solution")

        node = frontier.remove()

        if node.state == maze.get_goal():
            path = []
            while node.parent is not None:
                path_element = tuple([node.action, node.state])
                path.append(path_element)
                node = node.parent
            path.reverse()
            return path[:-1], explored[1:]

        explored_states.add(node.state)
        explored.append(node.state)

        for action, state in maze.get_next(node):
            if not frontier.contains_state(state) and state not in explored_states:
                child = Node(state=state, parent=node, action=action)
                frontier.add(child)


def greedy_first_search(start, maze):
    """
    Desc: Implements Greedy Best-First Search to find a path in the maze.
          It uses a heuristic to prioritize nodes closer to the goal.
    Parameters:
        start (tuple): The starting position as (row, col).
        maze (Maze): An instance of the Maze class.
    returns:
        (tuple): A list of actions leading from the start to the goal, guaranteed to be the shortest path.
                 AND. A list of all the explored states.
    """
    start = Node(state=start, parent=None, action=None)
    goal = maze.get_goal()
    func = manhattan_distance
    frontier = PriorityQueueFrontier(func, goal)  # Frontier with priority queue
    frontier.add(start)

    explored_states = set()
    explored = list()

    while True:
        if frontier.empty():
            raise Exception("No solution")

        node = frontier.remove()

        if node.state == goal:
            path = []
            while node.parent is not None:
                path_element = (node.action, node.state)
                path.append(path_element)
                node = node.parent
            path.reverse()
            return path[:-1], explored[1:]

        explored_states.add(node.state)
        explored.append(node.state)

        for action, state in maze.get_next(node):
            if not frontier.contains_state(state) and state not in explored_states:
                child = Node(state=state, parent=node, action=action)
                frontier.add(child)


def astar_first_search(start, maze):
    """
    Desc: Implements A* Search to find the shortest path in the maze.
          A* uses a combination of the actual path cost and a heuristic to efficiently find the optimal solution.
    Parameters:
        start (tuple): The starting position as (row, col).
        maze (Maze): An instance of the Maze class.
    returns:
        (tuple): A list of actions leading from the start to the goal, guaranteed to be the shortest path.
                 AND. A list of all the explored states.
    """
    start = CostNode(state=start, parent=None, action=None, cost=0)  # Cost is initialized to 0
    goal = maze.get_goal()
    func = cumulative_cost_function
    frontier = PriorityQueueFrontier(func, goal)  # Frontier with priority queue
    frontier.add(start)

    explored_states = set()
    explored = list()

    while True:
        if frontier.empty():
            raise Exception("No solution")

        node = frontier.remove()

        if node.state == goal:
            path = []
            while node.parent is not None:
                path_element = (node.action, node.state)
                path.append(path_element)
                node = node.parent
            path.reverse()
            return path[:-1], explored[1:]

        explored_states.add(node.state)
        explored.append(node.state)

        for action, state in maze.get_next(node):
            if not frontier.contains_state(state) and state not in explored_states:
                cost = node.cost + 1  # Increment cost for each step (assuming uniform cost)
                child = CostNode(state=state, parent=node, action=action, cost=cost)
                frontier.add(child)
