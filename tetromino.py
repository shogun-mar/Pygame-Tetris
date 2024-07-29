import pygame
from settings import TILE_SIZE, GRID_WIDTH, GRID_HEIGHT

class Tetromino:
    def __init__(self, screen, color, cell_positions, grid, highest_loose_cells_row):
        self.screen = screen
        self.color = color
        self.cell_positions = cell_positions
        self.grid = grid
        self.highest_loose_cells_row = highest_loose_cells_row

    def move_left(self):
        if self.can_move_left():
            self.cell_positions = [[cell[0] - 1, cell[1]] for cell in self.cell_positions]
 
    def can_move_left(self):
        leftmost_cell_column, leftmost_cell_row = min(self.cell_positions, key=lambda cell: cell[0])
        desired_leftmost_column = min(leftmost_cell_column - 1, 0)
        return not(self.is_right_above_loose_cells_or_bottom()) and self.grid[leftmost_cell_row][desired_leftmost_column] == 0 and desired_leftmost_column >= 0
        
    def move_right(self):
        if self.can_move_right():
            self.cell_positions = [[cell[0] + 1, cell[1]] for cell in self.cell_positions]

    def can_move_right(self):
        rightmost_cell_column, rightmost_cell_row = max(self.cell_positions, key=lambda cell: cell[0])
        desired_rightmost_column = rightmost_cell_column + 1
        return not(self.is_right_above_loose_cells_or_bottom()) and self.grid[rightmost_cell_row][min(rightmost_cell_column + 1, GRID_WIDTH - 1)] == 0 and desired_rightmost_column < GRID_WIDTH

    def is_right_above_loose_cells_or_bottom(self):
        lowermost_cell_row = max(cell[1] for cell in self.cell_positions)
        return (lowermost_cell_row == GRID_HEIGHT or lowermost_cell_row + 1 == self.highest_loose_cells_row)

    def move_down(self):
        self.cell_positions = [[cell[0], cell[1] + 1] for cell in self.cell_positions]

    def draw(self):
        for cell_position in self.cell_positions:
            column = cell_position[0]
            row = cell_position[1]
            pygame.draw.rect(self.screen, self.color, (column * TILE_SIZE, row * TILE_SIZE, TILE_SIZE, TILE_SIZE))

    def rotate_left(self):
        if self.can_move_left(): self._rotate(reverse_columns=True)

    def rotate_right(self):
        if self.can_move_right(): self._rotate(reverse_columns=False)

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