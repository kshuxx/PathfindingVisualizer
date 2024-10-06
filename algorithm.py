import pygame
import settings

# Constants for grid dimensions and offsets
NODE_SIZE = 24
GRID_OFFSET_X = 240
GRID_WIDTH = 52
GRID_HEIGHT = 30

class Algorithm:
    """Base class for all algorithms."""
    def __init__(self, pos_start: tuple, pos_end: tuple, wall_pos: list):
        self.pos_start = pos_start
        self.pos_end = pos_end
        self.wall_pos = wall_pos

class VisualisableAlgorithm(Algorithm):
    """Base class for all visualisable algorithms."""

    def __init__(self, app, pos_start: tuple, pos_end: tuple, wall_pos: list):
        super().__init__(pos_start, pos_end, wall_pos)
        self.app = app

    def draw_node(self, position: tuple, colour: tuple):
        """Draw a single node on the grid."""
        i, j = position
        pygame.draw.rect(self.app.screen, colour,
                         (i * NODE_SIZE + GRID_OFFSET_X, j * NODE_SIZE, NODE_SIZE, NODE_SIZE), 0)

    def draw_all_paths(self, position: tuple, colour: tuple):
        """Draw all paths and update the display."""
        self.draw_node(position, colour)

        # Redraw start/end nodes on top of all routes
        self.draw_node(self.pos_start, settings.TOMATO)
        self.draw_node(self.pos_end, settings.ROYALBLUE)

        # Redraw grid lines
        self.draw_grid()

        pygame.display.update()

    def draw_grid(self):
        """Draw the grid lines."""
        for x in range(GRID_WIDTH):
            pygame.draw.line(self.app.screen, settings.ALICE,
                             (settings.GS_X + x * NODE_SIZE, settings.GS_Y),
                             (settings.GS_X + x * NODE_SIZE, settings.GE_Y))
        for y in range(GRID_HEIGHT):
            pygame.draw.line(self.app.screen, settings.ALICE,
                             (settings.GS_X, settings.GS_Y + y * NODE_SIZE),
                             (settings.GE_X, settings.GS_Y + y * NODE_SIZE))
