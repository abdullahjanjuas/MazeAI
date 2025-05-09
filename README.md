# MazeAI

A Python-based project that implements various maze-solving algorithms, allowing for the analysis of different search strategies to solve mazes.

## Project Overview
This project provides a set of algorithms to solve mazes using different search strategies like Depth-First Search (DFS) Breadth-First Search (BFS), Greedy-First Search (GFS), and A*-First Search (AFS). It aims to help understand the differences in performance and behavior of these algorithms when solving various types of mazes.

## Features
- Random maze generation with different sizes, using backtracking (CSP).
- Solving mazes using BFS, DFS, GFS, and AFS search algorithms.
- Visual representation of maze and search process.
- Performance analysis and result comparison between different algorithms.
- Uses machine learning to predict best algorithm for a maze.

## Files
- `main.py`: The main entry point for running the maze-solving program.
- `maze.py`: Contains the logic to generate and represent the maze.
- `analysis.py`: Used for analyzing the results of maze-solving algorithms.
- `display.py`: Visualizes the maze and the solution.
- `search.py`: Implements search algorithms such as BFS, DFS, etc.
- `util.py`: Helper functions for maze generation and algorithm execution.
- `results.py`: Handles the logging and displaying of results.
- `train.py`: Generates data and trains an ML model.
- `model.py`: Uses trained model to solve maze.
- `requirements.txt`: Lists the necessary Python dependencies.

## Requirements
- Python 3.x
- Install required libraries:
  ```bash
  pip install -r requirements.txt
  ```

## Usage
Run the following command to start visualize the maze-solving process:
```bash
python3 main.py {rows} {cols}
```

Run the following to generate data using all search algorithms for randomly generated mazes
```bash
python3 analysis.py
```
Run the following to visualize these results
```bash
python3 results.py
```

Run the following file to generate 100,000 mazes and train a logistic regression model
```bash
python3 train.py
```

## License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.