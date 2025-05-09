"""
Author(s): 1. Hanzala B. Rehan
Description:
    This script reads the maze search results from a CSV file and visualizes the data using matplotlib.
    It generates plots for Manhattan Difference vs explored nodes/path length
    and Maze Size vs explored nodes/path length, showing them in a single figure.
Date created: November 22nd, 2024
Date last modified: November 22nd, 2024
"""

import pandas as pd  # Library for data manipulation
import matplotlib.pyplot as plt  # Library for creating visualizations
import seaborn as sns  # Library for enhanced visualization aesthetics


def visualize_results():
    """
    Reads the maze search results from a CSV file and visualizes the results using seaborn and matplotlib.
    It generates the following plots:
    - Manhattan Difference vs Number of Explored Nodes (all algorithms)
    - Manhattan Difference vs Path Length (all algorithms)
    - Maze Size vs Number of Explored Nodes (all algorithms)
    - Maze Size vs Path Length (all algorithms)
    Also includes A* specific plots when needed.
    """
    # Load the data from the CSV file
    df = pd.read_csv("maze_search_results.csv")

    # Add a new column for Maze Size (rows * cols)
    df['maze_size'] = df['rows'] * df['cols']

    # Set the seaborn style for better aesthetics
    sns.set(style="whitegrid")

    # Create a figure with subplots
    fig, axes = plt.subplots(2, 2, figsize=(14, 10))  # 2x2 grid for the plots
    plt.subplots_adjust(hspace=0.3, wspace=0.3)

    # Plot: Manhattan Difference vs Number of Explored Nodes (Line plot for all algorithms)
    sns.lineplot(data=df, x="manhattan_difference", y="bfs_explored_len", label="BFS", marker="o", ax=axes[0, 0])
    sns.lineplot(data=df, x="manhattan_difference", y="dfs_explored_len", label="DFS", marker="o", ax=axes[0, 0])
    sns.lineplot(data=df, x="manhattan_difference", y="gfs_explored_len", label="GFS", marker="o", ax=axes[0, 0])
    sns.lineplot(data=df, x="manhattan_difference", y="astar_explored_len", label="A*", marker="o", ax=axes[0, 0])
    axes[0, 0].set_xlabel("Manhattan Difference", fontsize=12)
    axes[0, 0].set_ylabel("Number of Explored Nodes", fontsize=12)
    axes[0, 0].set_title("Manhattan Difference vs Explored Nodes", fontsize=14)
    axes[0, 0].legend()

    # Plot: Manhattan Difference vs Path Length (Line plot for all algorithms)
    sns.lineplot(data=df, x="manhattan_difference", y="bfs_path_len", label="BFS", marker="o", ax=axes[0, 1])
    sns.lineplot(data=df, x="manhattan_difference", y="dfs_path_len", label="DFS", marker="o", ax=axes[0, 1])
    sns.lineplot(data=df, x="manhattan_difference", y="gfs_path_len", label="GFS", marker="o", ax=axes[0, 1])
    sns.lineplot(data=df, x="manhattan_difference", y="astar_path_len", label="A*", marker="o", ax=axes[0, 1])
    axes[0, 1].set_xlabel("Manhattan Difference", fontsize=12)
    axes[0, 1].set_ylabel("Path Length", fontsize=12)
    axes[0, 1].set_title("Manhattan Difference vs Path Length", fontsize=14)
    axes[0, 1].legend()

    # Plot: Maze Size vs Number of Explored Nodes (Line plot for all algorithms)
    sns.lineplot(data=df, x="maze_size", y="bfs_explored_len", label="BFS", marker="o", ax=axes[1, 0])
    sns.lineplot(data=df, x="maze_size", y="dfs_explored_len", label="DFS", marker="o", ax=axes[1, 0])
    sns.lineplot(data=df, x="maze_size", y="gfs_explored_len", label="GFS", marker="o", ax=axes[1, 0])
    sns.lineplot(data=df, x="maze_size", y="astar_explored_len", label="A*", marker="o", ax=axes[1, 0])
    axes[1, 0].set_xlabel("Maze Size (rows * cols)", fontsize=12)
    axes[1, 0].set_ylabel("Number of Explored Nodes", fontsize=12)
    axes[1, 0].set_title("Maze Size vs Explored Nodes", fontsize=14)
    axes[1, 0].legend()

    # Plot: Maze Size vs Path Length (Line plot for all algorithms)
    sns.lineplot(data=df, x="maze_size", y="bfs_path_len", label="BFS", marker="o", ax=axes[1, 1])
    sns.lineplot(data=df, x="maze_size", y="dfs_path_len", label="DFS", marker="o", ax=axes[1, 1])
    sns.lineplot(data=df, x="maze_size", y="gfs_path_len", label="GFS", marker="o", ax=axes[1, 1])
    sns.lineplot(data=df, x="maze_size", y="astar_path_len", label="A*", marker="o", ax=axes[1, 1])
    axes[1, 1].set_xlabel("Maze Size (rows * cols)", fontsize=12)
    axes[1, 1].set_ylabel("Path Length", fontsize=12)
    axes[1, 1].set_title("Maze Size vs Path Length", fontsize=14)
    axes[1, 1].legend()

    # Show all the plots
    plt.show()

    # If you want to save the figure with all plots
    fig.savefig("Results.png", bbox_inches='tight')


if __name__ == "__main__":
    visualize_results()
