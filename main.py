"""
Author(s): 1. Hanzala B. Rehan
Description: Main Entry point for this project
Date created: November 15th, 2024
Date last modified: November 22nd, 2024
"""

import argparse
from maze import Maze
from display import GridDisplay


def main():
    """
    Desc: Parses command-line arguments and generates a maze.
    """
    parser = argparse.ArgumentParser(description="Generate a random solvable maze.")
    parser.add_argument('rows', type=int, help="Number of rows for the maze.")
    parser.add_argument('cols', type=int, help="Number of columns for the maze.")

    args = parser.parse_args()

    maze = Maze(args.rows, args.cols)
    grid = GridDisplay(maze)
    grid.run()


if __name__ == "__main__":
    main()
