"""
Author(s): 1. Hanzala B. Rehan
Description: This script generates random mazes, performs various search algorithms (BFS, DFS, GFS, A*),
             collects performance metrics, and saves the results in a CSV file.
             Then it trains a logistic regression model, which it save in a joblib file.
Date created: May 6th, 2025
Date last modified: May 6th, 2025
"""
import numpy as np
import joblib
from features import calculate_maze_density, compute_branching_factor, count_dead_ends
from util import manhattan_distance, Node

def best_algo(maze):
    """
    Predicts the best pathfinding algorithm for a given maze using a trained model.
    
    Args:
        maze: Maze object containing the grid, start, and goal positions
        
    Returns:
        str: Name of the recommended algorithm ('BFS', 'DFS', 'GFS', or 'AFS')
    """
    # Extract maze features
    rows = maze.rows
    cols = maze.cols

    start = Node(maze.start, None, None)
    goal = maze.get_goal()
    distance = manhattan_distance(start, goal)

    density = calculate_maze_density(maze)
    dead_ends = count_dead_ends(maze)
    branching = compute_branching_factor(maze)
    
    # Create feature vector
    features = np.array([[rows, cols, distance, density, dead_ends, branching]])
    
    try:
        # Load trained model and label encoder
        model_data = joblib.load('model.joblib')
        model = model_data['model']
        encoder = model_data['encoder']
        
        # Make prediction
        prediction = model.predict(features)
        best_algorithm = encoder.inverse_transform(prediction)[0]
        
        return best_algorithm
    except FileNotFoundError:
        raise FileNotFoundError("Model file 'model.joblib' not found. Please train the model first.")
    except Exception as e:
        raise RuntimeError(f"Error making prediction: {str(e)}")