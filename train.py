"""
Author(s): 1. Hanzala B. Rehan
Description: This script generates random mazes, performs various search algorithms (BFS, DFS, GFS, A*),
             collects performance metrics, and saves the results in a CSV file.
             Then it trains a logistic regression model, which it save in a joblib file.
Date created: May 5th, 2025
Date last modified: May 5th, 2025
"""
import pandas as pd
import numpy as np
import random
import time

from maze import Maze
from search import (
    breadth_first_search, 
    depth_first_search, 
    greedy_first_search, 
    astar_first_search
)
from util import manhattan_distance, Node
from features import calculate_maze_density, count_dead_ends, compute_branching_factor

from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.metrics import classification_report
from sklearn.pipeline import make_pipeline
from sklearn.model_selection import GridSearchCV

import joblib


def choose_best_algorithm(results):
    """
    Chooses the best algorithm based on a weighted sum:
    0.7 * shortest path length + 0.3 * number of nodes explored.

    Parameters:
        results (dict): A dictionary with keys as algorithm names and values as
                        (explored_len, path_len) tuples.
    
    Returns:
        str: The name of the best algorithm (e.g., 'BFS', 'DFS', etc.)
    """
    weighted_scores = {
        algo: 0.5 * path_len + 0.5 * explored_len
        for algo, (explored_len, path_len) in results.items()
    }
    return min(weighted_scores, key=weighted_scores.get)


def generate_maze_dataset(num_samples=10000, save_path="Maze_Dataset.csv"):
    """Generates dataset with engineered features."""
    df = pd.DataFrame(columns=[
        "rows", "cols", "manhattan_distance",
        "maze_density", "dead_ends", "branching_factor",
        "label"
    ])

    for i in range(num_samples):
        if i % 1000 == 0:
            print(f"Processing Maze {i + 1}/{num_samples}")

        rows = cols = random.randint(5, 15) #, 
        random.randint(5, 15)
        maze = Maze(rows, cols)  # Assumes maze.grid uses '#', ' ', 'S', 'G'

        start = Node(maze.start, None, None)
        goal = maze.get_goal()
        manhattan = manhattan_distance(start, goal)

        density = calculate_maze_density(maze)
        dead_ends = count_dead_ends(maze)
        branching = compute_branching_factor(maze)

        bfs_explored, bfs_path = breadth_first_search(maze.start, maze)
        dfs_explored, dfs_path = depth_first_search(maze.start, maze)
        gfs_explored, gfs_path = greedy_first_search(maze.start, maze)
        afs_explored, afs_path = astar_first_search(maze.start, maze)

        results = {
            "BFS": (len(bfs_explored) + 1, len(bfs_path)),
            "AFS": (len(afs_explored) + 1, len(afs_path)),
            "DFS": (len(dfs_explored) + 1, len(dfs_path)),
            "GFS": (len(gfs_explored) + 1, len(gfs_path)),
        }
        best_algo = choose_best_algorithm(results)

        df.loc[len(df)] = [
            rows, cols, manhattan,
            density, dead_ends, branching,
            best_algo
        ]

    df.to_csv(save_path, index=False)
    print(f"Dataset saved to {save_path}")


def train_model(csv_path="Maze_Dataset.csv"):
    """
    Desc: Loads maze dataset from a CSV, encodes labels, trains a logistic regression model,
          and prints evaluation results.

          Training function with feature scaling, better model selection,
          and hyperparameter tuning to improve accuracy.
    

    Parameters:
        csv_path (str): Path to the CSV file with maze data.

    Returns:
        model (LogisticRegression): Trained logistic regression model.
    """
    # Load and prepare data
    df = pd.read_csv(csv_path)
    
    # Features and target
    X = df[["rows", "cols", "manhattan_distance", 
            "maze_density", "dead_ends", "branching_factor"]]
    y = df["label"]
    
    # Encode labels
    encoder = LabelEncoder()
    y_encoded = encoder.fit_transform(y)
    
    # Train-test split with stratification
    X_train, X_test, y_train, y_test = train_test_split(
        X, y_encoded, test_size=0.2, random_state=42, stratify=y_encoded
    )
    
    # Create preprocessing and modeling pipeline
    pipeline = make_pipeline(
        StandardScaler(),
        LogisticRegression(max_iter=1000, class_weight='balanced')
    )
    
    # Hyperparameter tuning
    param_grid = {
        'logisticregression__C': [0.001, 0.01, 0.1, 1, 10, 100],
        'logisticregression__solver': ['lbfgs', 'liblinear']
    }
    
    # Grid search with cross-validation
    grid_search = GridSearchCV(
        pipeline,
        param_grid,
        cv=5,
        scoring='accuracy',
        n_jobs=-1
    )
    grid_search.fit(X_train, y_train)
    
    # Best model
    best_model = grid_search.best_estimator_
    
    # Evaluation
    y_pred = best_model.predict(X_test)
    print(f"Best Parameters: {grid_search.best_params_}")
    print("Classification Report:\n",
          classification_report(y_test, y_pred,
                               labels=encoder.transform(encoder.classes_),
                               target_names=encoder.classes_))
    
    # Save model and encoder
    joblib.dump({'model': best_model, 'encoder': encoder}, 'maze_model.joblib')
    
    return best_model

if __name__ == "__main__":
    generate_maze_dataset(100000)
    time.sleep(1)
    train_model()
