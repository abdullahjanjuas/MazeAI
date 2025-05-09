"""
Author(s): 1. Hanzala B. Rehan
Description: This script generates random mazes, performs various search algorithms (BFS, DFS, GFS, A*),
             collects performance metrics, and saves the results in a CSV file.
Date created: November 22nd, 2024
Date last modified: November 22nd, 2024
"""
import pandas as pd
import numpy as np
import random
from maze import Maze
from search import breadth_first_search, depth_first_search, greedy_first_search, astar_first_search
from util import manhattan_distance, Node


def analyze_results():
    """
    Main function to generate random mazes, perform search algorithms on them,
    collect results, and save them into a CSV file.
    """
    # Create an empty DataFrame with appropriate column names
    df = pd.DataFrame(columns=[
        "rows", "cols", "manhattan_difference",
        "bfs_explored_len", "bfs_path_len",
        "dfs_explored_len", "dfs_path_len",
        "gfs_explored_len", "gfs_path_len",
        "astar_explored_len", "astar_path_len"
    ])

    for i in range(10):
        print(f"Searching Maze {i + 1}")
        # Generate random maze dimensions
        num_rows = random.randint(3, 20)
        num_cols = random.randint(3, 20)

        # Create a maze and extract start and goal positions
        maze = Maze(num_rows, num_rows)
        start = Node(maze.start, None, None)
        goal = maze.get_goal()
        grid = np.array(maze.get_maze())

        # Calculate Manhattan difference
        manhattan_difference = manhattan_distance(start, goal)

        # Perform searches and calculate explored and path lengths
        bfs_explored, bfs_path = breadth_first_search(maze.start, maze)
        bfs_explored_len, bfs_path_len = len(bfs_explored) + 1, len(bfs_path)

        dfs_explored, dfs_path = depth_first_search(maze.start, maze)
        dfs_explored_len, dfs_path_len = len(dfs_explored) + 1, len(dfs_path)

        gfs_explored, gfs_path = greedy_first_search(maze.start, maze)
        gfs_explored_len, gfs_path_len = len(gfs_explored) + 1, len(gfs_path)

        astar_explored, astar_path = astar_first_search(maze.start, maze)
        astar_explored_len, astar_path_len = len(astar_explored) + 1, len(astar_path)

        # Append the results directly to the DataFrame
        df = pd.concat([df, pd.DataFrame([{
            "rows": num_rows,
            "cols": num_cols,
            "manhattan_difference": manhattan_difference,
            "bfs_explored_len": bfs_explored_len,
            "bfs_path_len": bfs_path_len,
            "dfs_explored_len": dfs_explored_len,
            "dfs_path_len": dfs_path_len,
            "gfs_explored_len": gfs_explored_len,
            "gfs_path_len": gfs_path_len,
            "astar_explored_len": astar_explored_len,
            "astar_path_len": astar_path_len
        }])], ignore_index=True)

    # Save the DataFrame to a CSV file
    df.to_csv("maze_search_results.csv", index=False)
    print("Results saved to maze_search_results.csv")


if __name__ == "__main__":
    analyze_results()
