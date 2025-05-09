"""
Author(s): 1. Hanzala B. Rehan
Description: A script to display a 2D grid represented as a list of characters using pygame, implemented as a class,
            with buttons for search algorithms.
Date created: November 15th, 2024
Date last modified: May 6th, 2024
"""

import pygame
from maze import Maze
from search import breadth_first_search, depth_first_search, greedy_first_search, astar_first_search
from model import best_algo


class GridDisplay:
    """
    Desc: Class to handle the display of a 2D grid using pygame, with interactive buttons.
    """

    TILE_SIZE = 40                      # Size of each grid tile
    PADDING = 40                        # Padding around the grid
    BUTTON_WIDTH = 75                   # Width of buttons
    BUTTON_HEIGHT = 75                  # Height of buttons
    BUTTON_PADDING = 10                 # Spacing between buttons

    # Colors
    COLOR_WALL = (30, 30, 30)           # Black for walls
    COLOR_PATH = (244, 246, 255)        # White for paths
    COLOR_START = (235, 45, 45)         # Red for start
    COLOR_GOAL = (79, 174, 31)          # Green for goal
    COLOR_BG = (0, 0, 0)                # Black background
    COLOR_BORDER = (0, 0, 0)            # Black border for tiles
    COLOR_EXPLORED = (218, 240, 100)    # Light Red for explored tiles
    COLOR_PATH_TILE = (210, 80, 73)     # Yellow for path tiles
    COLOR_BUTTON = (100, 100, 255)      # Blue for buttons
    COLOR_BUTTON_HOVER = (50, 50, 200)  # Darker blue for hovered buttons
    COLOR_TEXT = (255, 255, 255)        # White text

    STRING = "MAZE AI"

    def __init__(self, maze):
        """
        Desc: Initializes the GridDisplay class.
        Parameters:
            maze (Maze): 2D grid representation.
        """
        self.maze = maze
        self.start = maze.start
        self.grid = maze.get_maze()
        self.grid_width = len(self.grid[0])
        self.grid_height = len(self.grid)
        self.screen_width = (
            self.grid_width * self.TILE_SIZE
            + 2 * self.PADDING
            + self.BUTTON_WIDTH
            + self.BUTTON_PADDING
        )
        self.screen_height = max(
            self.grid_height * self.TILE_SIZE
            + 2 * self.PADDING + 30,
            4 * self.BUTTON_HEIGHT
            + 5 * self.BUTTON_PADDING + 30,
        ) # Additional 30 for Text

        # Initialize pygame and set up display
        pygame.init()
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        self.font = pygame.font.Font(None, 48)
        pygame.display.set_caption("AI Maze Solver")

        # Button positions
        self.buttons = {
            "DFS": pygame.Rect(
                self.BUTTON_PADDING,
                self.BUTTON_PADDING,
                self.BUTTON_WIDTH,
                self.BUTTON_HEIGHT,
            ),
            "BFS": pygame.Rect(
                self.BUTTON_PADDING,
                self.BUTTON_PADDING * 2 + self.BUTTON_HEIGHT,
                self.BUTTON_WIDTH,
                self.BUTTON_HEIGHT,
            ),
            "GFS": pygame.Rect(
                self.BUTTON_PADDING,
                self.BUTTON_PADDING * 3 + self.BUTTON_HEIGHT * 2,
                self.BUTTON_WIDTH,
                self.BUTTON_HEIGHT,
            ),
            "AFS": pygame.Rect(
                self.BUTTON_PADDING,
                self.BUTTON_PADDING * 4 + self.BUTTON_HEIGHT * 3,
                self.BUTTON_WIDTH,
                self.BUTTON_HEIGHT,
            ),
            "ML": pygame.Rect(
                self.BUTTON_PADDING,
                self.BUTTON_PADDING * 5 + self.BUTTON_HEIGHT * 4,
                self.BUTTON_WIDTH,
                self.BUTTON_HEIGHT,
            ),
            "Reset": pygame.Rect(
                self.BUTTON_PADDING,
                self.BUTTON_PADDING * 6 + self.BUTTON_HEIGHT * 5,
                self.BUTTON_WIDTH,
                self.BUTTON_HEIGHT,
            ),
        }

        # Font for buttons
        self.font = pygame.font.Font(None, 24)

        # Lists to track explored and path tiles
        self.explored_tiles = []
        self.path_tiles = []

    def draw_buttons(self):
        """
        Desc: Draw buttons for DFS, BFS, GFS, and AFS on the screen.
        returns:
        None
        """
        for label, rect in self.buttons.items():
            # Detect mouse hover
            mouse_pos = pygame.mouse.get_pos()
            color = self.COLOR_BUTTON_HOVER if rect.collidepoint(mouse_pos) else self.COLOR_BUTTON

            # Draw button and label
            pygame.draw.rect(self.screen, color, rect)
            pygame.draw.rect(self.screen, self.COLOR_BORDER, rect, 2)
            text = self.font.render(label, True, self.COLOR_TEXT)
            text_rect = text.get_rect(center=rect.center)
            self.screen.blit(text, text_rect)

    def draw_grid(self):
        """
        Desc: Draw the grid on the screen based on the predefined grid and overlay explored/path tiles.
        returns:
        None
        """
        # Draw padding (background)
        self.screen.fill(self.COLOR_BG)

        # Draw the grid tiles
        for row in range(self.grid_height):
            for col in range(self.grid_width):
                rect = pygame.Rect(
                    self.PADDING + self.BUTTON_WIDTH + self.BUTTON_PADDING + col * self.TILE_SIZE,
                    self.PADDING + row * self.TILE_SIZE,
                    self.TILE_SIZE,
                    self.TILE_SIZE,
                )
                if self.grid[row][col] == "#":
                    pygame.draw.rect(self.screen, self.COLOR_WALL, rect)
                elif self.grid[row][col] == " ":
                    pygame.draw.rect(self.screen, self.COLOR_PATH, rect)
                elif self.grid[row][col] == "S":
                    pygame.draw.rect(self.screen, self.COLOR_START, rect)
                elif self.grid[row][col] == "G":
                    pygame.draw.rect(self.screen, self.COLOR_GOAL, rect)

                pygame.draw.rect(self.screen, self.COLOR_BORDER, rect, 1)

        # Overlay explored tiles
        for y, x in self.explored_tiles:
            rect = pygame.Rect(
                self.PADDING + self.BUTTON_WIDTH + self.BUTTON_PADDING + x * self.TILE_SIZE,
                self.PADDING + y * self.TILE_SIZE,
                self.TILE_SIZE,
                self.TILE_SIZE,
            )
            pygame.draw.rect(self.screen, self.COLOR_EXPLORED, rect)
            pygame.draw.rect(self.screen, self.COLOR_BORDER, rect, 1)

        # Overlay path tiles
        for (ac, (y, x)) in self.path_tiles:
            rect = pygame.Rect(
                self.PADDING + self.BUTTON_WIDTH + self.BUTTON_PADDING + x * self.TILE_SIZE,
                self.PADDING + y * self.TILE_SIZE,
                self.TILE_SIZE,
                self.TILE_SIZE,
            )
            pygame.draw.rect(self.screen, self.COLOR_PATH_TILE, rect)
            pygame.draw.rect(self.screen, self.COLOR_BORDER, rect, 1)

    def explore_maze(self, path):
        """
        Desc: Change the color of tiles along a given path to indicate they have been explored.
        Parameters:
            path (list of tuple): A list of (x, y) coordinates representing the path to explore.
        returns:
            None
        """
        self.explored_tiles.extend(path)
        for y, x in path:
            rect = pygame.Rect(
                self.PADDING + self.BUTTON_WIDTH + self.BUTTON_PADDING + x * self.TILE_SIZE,
                self.PADDING + y * self.TILE_SIZE,
                self.TILE_SIZE,
                self.TILE_SIZE,
            )
            pygame.draw.rect(self.screen, self.COLOR_EXPLORED, rect)
            pygame.draw.rect(self.screen, self.COLOR_BORDER, rect, 1)
            pygame.display.flip()

    def draw_path(self, path):
        """
        Desc: Change the color of all tiles in the given path to indicate the path.
        Parameters:
            path (list of tuple): A list of (x, y) coordinates representing the path.
        returns:
            None
        """
        self.path_tiles.extend(path)
        for (ac, (y, x)) in path:
            rect = pygame.Rect(
                self.PADDING + self.BUTTON_WIDTH + self.BUTTON_PADDING + x * self.TILE_SIZE,
                self.PADDING + y * self.TILE_SIZE,
                self.TILE_SIZE,
                self.TILE_SIZE,
            )
            pygame.draw.rect(self.screen, self.COLOR_PATH_TILE, rect)
            pygame.draw.rect(self.screen, self.COLOR_BORDER, rect, 1)
            pygame.display.flip()

    def reset(self):
        """
        Desc: Resets the grid, clearing the explored and path tiles.
        returns:
            None
        """
        self.explored_tiles = []
        self.path_tiles = []
        self.grid = self.maze.get_maze()
        self.start = self.maze.start
        self.draw_grid()

    def search(self, label):
        if label == "ML":
            self.STRING = "ALGO: COMPUTING..."
            label = best_algo(self.maze)

        if label == "DFS":
            self.STRING = "ALGO: DFS"
            path, explored = depth_first_search(self.start, self.maze)
            for tile in explored:
                self.explore_maze([tile])
                pygame.time.delay(50)

            self.draw_path(path)

        elif label == "BFS":
            self.STRING = "ALGO: BFS"
            path, explored = breadth_first_search(self.start, self.maze)
            for tile in explored:
                self.explore_maze([tile])
                pygame.time.delay(50)

            self.draw_path(path)

        elif label == "GFS":
            self.STRING = "ALGO: GFS"
            path, explored = greedy_first_search(self.start, self.maze)
            for tile in explored:
                self.explore_maze([tile])
                pygame.time.delay(50)

            self.draw_path(path)

        elif label == "AFS":
            self.STRING = "ALGO: AFS"
            path, explored = astar_first_search(self.start, self.maze)
            for tile in explored:
                self.explore_maze([tile])
                pygame.time.delay(50)

            self.draw_path(path)


    def run(self):
        """
        Desc: Runs the pygame loop to display the grid and buttons.
        returns:
        None
        """
        running = True
        clock = pygame.time.Clock()

        while running:
            title_text = self.font.render(self.STRING, True, pygame.Color("Green"))
            title_rect = title_text.get_rect(center=(self.screen.get_width() // 2, self.screen_height - 35))

            self.screen.fill(self.COLOR_BG)
            self.draw_grid()
            self.draw_buttons()
            self.screen.blit(title_text, title_rect)
            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = pygame.mouse.get_pos()
                    for label, rect in self.buttons.items():
                        if rect.collidepoint(mouse_pos):
                            if label == "Reset":
                                self.reset()
                            else:
                                self.search(label)

            clock.tick(30)

        pygame.quit()
