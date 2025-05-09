"""
Author(s):  1. Hanzala B. Rehan
Description: This script defines a class `Maze` which generates a random,
            solvable maze using Depth-First Search (DFS) algorithm.
Date created: November 15th, 2024
Date last modified: May 5th, 2025
"""


import random
from util import Node
from collections import deque
import random


class Maze:
    # Constructor to initialize the maze with given rows and columns.
    def __init__(self, rows, cols):
        """
        Desc: Initializes the maze with the specified number of rows and columns.
        Parameters:
            rows (int): Odd number of rows in the maze.
            cols (int): Odd number of columns in the maze.
        """
        self.goal = None
        self.start = None
        self.rows = rows if rows % 2 == 1 else rows + 1  # Number of rows, Ensuring odd number of rows.
        self.cols = cols if cols % 2 == 1 else cols + 1  # Number of columns, Ensuring odd number of rows.
        self.maze = self.generate_solvable_maze()  # Generates a solvable maze upon initialization

    def generate_solvable_maze(self):
        """
        Generates a more complex and less predictable maze using a modified DFS algorithm.
        Returns a 2D list representing the maze with:
            'S' = start, 'G' = goal, ' ' = path, '#' = wall
        """
        # Ensure odd dimensions for proper path spacing
        self.rows |= 1
        self.cols |= 1

        # Initialize all cells as walls
        maze = [['#' for _ in range(self.cols)] for _ in range(self.rows)]

        # Choose a random odd cell to start
        start_row = random.randrange(1, self.rows, 2)
        start_col = random.randrange(1, self.cols, 2)
        maze[start_row][start_col] = 'S'
        self.start = (start_row, start_col)

        # DFS stack and directions
        stack = [(start_row, start_col)]
        directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]  # R, D, L, U

        while stack:
            r, c = stack.pop()

            # Bias toward branching: avoid too long corridors
            biased_dirs = sorted(directions, key=lambda _: random.random() + 0.2 * random.randint(0, 1))
            for dr, dc in biased_dirs:
                nr, nc = r + dr * 2, c + dc * 2

                if 0 <= nr < self.rows and 0 <= nc < self.cols and maze[nr][nc] == '#':
                    maze[r + dr][c + dc] = ' '  # Path between
                    maze[nr][nc] = ' '          # Target cell
                    stack.append((nr, nc))

        # Replace 'S' with ' ' temporarily to find goal
        maze[start_row][start_col] = ' '
        goal_row, goal_col = self.find_farthest_point(maze, (start_row, start_col))
        maze[goal_row][goal_col] = 'G'
        self.goal = (goal_row, goal_col)

        # Set start point back
        maze[start_row][start_col] = 'S'

        return maze

    @staticmethod
    def find_farthest_point(maze, start):
        """Finds the farthest reachable cell from the start using BFS."""
        visited = set()
        queue = deque([(start[0], start[1], 0)])
        farthest = start
        max_dist = -1

        while queue:
            r, c, dist = queue.popleft()
            if (r, c) in visited:
                continue
            visited.add((r, c))

            if dist > max_dist:
                max_dist = dist
                farthest = (r, c)

            for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                nr, nc = r + dr, c + dc
                if 0 <= nr < len(maze) and 0 <= nc < len(maze[0]) and maze[nr][nc] == ' ':
                    queue.append((nr, nc, dist + 1))

        return farthest

    def generate_maze(self):
        """
        Desc: Generates a random maze using Prim's algorithm.
            Starts from a random position, carves paths by expanding into nearby walls, 
            and places the goal in a reachable open space.
        
        returns:
        (list): A 2D list representing the maze layout where:
                '#' is a wall,
                ' ' is a free path,
                'S' is the start point, and
                'G' is the goal point.
        """
        # Pick a random starting point (odd-indexed to ensure it's inside the grid)
        r, c = random.randrange(1, self.rows, 2), random.randrange(1, self.cols, 2)
        maze = [['#' for _ in range(self.cols)] for _ in range(self.rows)]
        maze[r][c] = 'S'  # Set starting cell
        self.start = (r, c)

        # Add neighboring walls (two steps away) to the wall list
        walls = []
        for dr, dc in [(-2, 0), (2, 0), (0, -2), (0, 2)]:
            nr, nc = r + dr, c + dc
            if 1 <= nr < self.rows - 1 and 1 <= nc < self.cols - 1:
                walls.append((r + dr, c + dc, dr, dc))

        # Loop until all reachable walls are processed
        while walls:
            # Randomly pick a wall
            wr, wc, dr, dc = walls.pop(random.randint(0, len(walls) - 1))
            r, c = wr - dr, wc - dc

            # Skip if already connected or visited
            if maze[wr][wc] == '#' and maze[r][c] == ' ':
                continue

            if maze[wr][wc] == '#':
                # Carve path between current cell and wall
                maze[wr - dr // 2][wc - dc // 2] = ' '
                maze[wr][wc] = ' '

                # Add neighboring walls of the newly carved cell
                for ddr, ddc in [(-2, 0), (2, 0), (0, -2), (0, 2)]:
                    nr, nc = wr + ddr, wc + ddc
                    if 1 <= nr < self.rows - 1 and 1 <= nc < self.cols - 1 and maze[nr][nc] == '#':
                        walls.append((wr + ddr, wc + ddc, ddr, ddc))

        # Pick a random open cell as the goal (not the start)
        empty_spaces = [(r, c) for r in range(self.rows) for c in range(self.cols) if maze[r][c] == ' ']
        goal_row, goal_col = random.choice(empty_spaces)
        maze[goal_row][goal_col] = 'G'
        self.goal = (goal_row, goal_col)

        return maze


    def print_maze(self):
        """
        Desc: Prints the maze in a visually clear format.
        """
        for row in self.maze:
            print("".join(row))  # Join each row list and print as a string

    def get_maze(self):
        """
        Desc: Returns the maze layout.
        returns:
        (list): The maze as a 2D list.
        """
        return self.maze

    def get_goal(self):
        """
        Desc: Returns the maze layout.
        returns:
        (tuple): x, y coordinates of the goal
        """
        return self.goal

    def is_goal(self, node):
        """
        Desc: Returns the maze layout.
        Parameters:
            node (Node): the node to check
        returns:
        (bool): True if node is at goal.
        """
        if node.state == self.goal:
            return True
        return False

    def get_next(self, node):
        """
        Desc: Returns the next nodes available through legal moves
        Parameters:
            node (Node): the node to check
        returns:
        (list): A list of tuples representing the next valid states and actions.
                Each tuple contains (action, next_state), where:
                    action (str): The move direction ('left', 'right', 'up', 'down').
                    next_state (tuple): The (row, col) coordinates of the next position.
        """
        # Define possible moves and their corresponding actions
        moves = {
            'left': (0, -1),
            'right': (0, 1),
            'up': (-1, 0),
            'down': (1, 0)
        }

        next_nodes = []  # List to store valid next nodes

        for action, (dr, dc) in moves.items():
            next_row, next_col = node.state[0] + dr, node.state[1] + dc

            # Check if the next move is within bounds and not hitting a wall
            if 0 <= next_row < self.rows and 0 <= next_col < self.cols and self.maze[next_row][next_col] != '#':
                next_nodes.append((action, (next_row, next_col)))  # Add valid move

        return next_nodes  # Return all valid moves
