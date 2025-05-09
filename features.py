"""
Author(s): 1. Hanzala B. Rehan
Description: This script contains functions to generate features for a given maze. To support Machine Learning.
Date created: May 5th, 2025
Date last modified: May 5th, 2025
"""
from maze import Maze

def calculate_maze_density(maze):
    """Calculates the ratio of walls to total cells."""
    walls = sum(sum(1 for cell in row if cell == '#') for row in maze.maze)
    return walls / (maze.rows * maze.cols)


def count_dead_ends(maze):
    """Counts cells with only one open neighbor (dead ends)."""
    dead_ends = 0
    for i in range(maze.rows):
        for j in range(maze.cols):
            if maze.maze[i][j] in {' ', 'S', 'G'}:  # Only check open paths
                neighbors = 0
                for di, dj in [(-1,0), (1,0), (0,-1), (0,1)]:
                    ni, nj = i + di, j + dj
                    if 0 <= ni < maze.rows and 0 <= nj < maze.cols:
                        if maze.maze[ni][nj] in {' ', 'S', 'G'}:
                            neighbors += 1
                if neighbors == 1:
                    dead_ends += 1
    return dead_ends


def compute_branching_factor(maze):
    """Computes average number of choices per open cell."""
    total_choices = 0
    open_cells = 0
    for i in range(maze.rows):
        for j in range(maze.cols):
            if maze.maze[i][j] in {' ', 'S', 'G'}:
                choices = 0
                for di, dj in [(-1,0), (1,0), (0,-1), (0,1)]:
                    ni, nj = i + di, j + dj
                    if 0 <= ni < maze.rows and 0 <= nj < maze.cols:
                        if maze.maze[ni][nj] in {' ', 'S', 'G'}:
                            choices += 1
                total_choices += choices
                open_cells += 1
    return total_choices / open_cells if open_cells else 0