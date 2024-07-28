import pygame
from settings import TILE_SIZE, GRID_WIDTH

class Tetromino:
    def __init__(self, screen, color, cell_positions):
        self.screen = screen
        self.color = color
        self.cell_positions = cell_positions

    def move_left(self):
        leftmost_column = min(cell[0] for cell in self.cell_positions)
        if leftmost_column > 0:
            self.cell_positions = [[cell[0] - 1, cell[1]] for cell in self.cell_positions]
    
    def move_right(self):
        rightmost_column = max(cell[0] for cell in self.cell_positions)
        if rightmost_column < GRID_WIDTH - 1:
            self.cell_positions = [[cell[0] + 1, cell[1]] for cell in self.cell_positions]

    def move_down(self):
        self.cell_positions = [[cell[0], cell[1] + 1] for cell in self.cell_positions]

    def draw(self):
        for cell_position in self.cell_positions:
            column = cell_position[0]
            row = cell_position[1]
            pygame.draw.rect(self.screen, self.color, (column * TILE_SIZE, row * TILE_SIZE, TILE_SIZE, TILE_SIZE))

    def rotate_left(self):
        self._rotate(reverse_columns=True)

    def rotate_right(self):
        self._rotate(reverse_columns=False)

    def _rotate(self, reverse_columns):
        # Calculate the bounding box of the tetromino
        min_x = min(cell[0] for cell in self.cell_positions)
        max_x = max(cell[0] for cell in self.cell_positions)
        min_y = min(cell[1] for cell in self.cell_positions)
        max_y = max(cell[1] for cell in self.cell_positions)

        # Calculate the center of the bounding box
        center_x = (min_x + max_x) // 2
        center_y = (min_y + max_y) // 2

        # Translate cells to origin
        translated_positions = [[cell[0] - center_x, cell[1] - center_y] for cell in self.cell_positions]

        # Rotate cells
        if reverse_columns:
            rotated_positions = [[-cell[1], cell[0]] for cell in translated_positions]
        else:
            rotated_positions = [[cell[1], -cell[0]] for cell in translated_positions]

        # Translate cells back to their original position
        self.cell_positions = [[cell[0] + center_x, cell[1] + center_y] for cell in rotated_positions]

    def to_matrix(self, positions):
        # Convert list of positions to a matrix representation
        max_x = max(pos[0] for pos in positions)
        max_y = max(pos[1] for pos in positions)
        matrix = [[0] * (max_x + 1) for _ in range(max_y + 1)]
        for pos in positions:
            matrix[pos[1]][pos[0]] = 1
        return matrix

    def transpose(self, matrix):
        # Transpose the matrix
        return [list(row) for row in zip(*matrix)]