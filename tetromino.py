import pygame
from settings import *

class Tetromino:
    def __init__(self, screen, cell_positions, color):
        self.screen = screen
        self.cell_positions = cell_positions
        self.color = color

    def move_down(self):
        for cell_position in self.cell_positions:
            cell_position[1] += 1

    def move_left(self):
        for cell_position in self.cell_positions:
            cell_position[0] -= 1

    def move_right(self):
        for cell_position in self.cell_positions:
            cell_position[0] += 1

    def rotate_left(self):
        def reverse_columns(matrix):
            return [list(reversed(row)) for row in matrix]

        matrix = self.to_matrix(self.cell_positions)
        transposed_matrix = self.transpose(matrix)
        rotated_matrix = reverse_columns(transposed_matrix)
        self.cell_positions = self.from_matrix(rotated_matrix)

    def rotate_right(self):
        def reverse_rows(matrix):
            return [list(row) for row in reversed(matrix)]

        matrix = self.to_matrix(self.cell_positions)
        transposed_matrix = self.transpose(matrix)
        rotated_matrix = reverse_rows(transposed_matrix)
        self.cell_positions = self.from_matrix(rotated_matrix)

    def draw(self):
        for cell_position in self.cell_positions:
            column = cell_position[0]
            row = cell_position[1]
            pygame.draw.rect(self.screen, self.color, (column * TILE_SIZE, row * TILE_SIZE, TILE_SIZE, TILE_SIZE))

    def to_matrix(self, cell_positions):
            max_x = max(cell[0] for cell in cell_positions)
            max_y = max(cell[1] for cell in cell_positions)
            matrix = [[0] * (max_x + 1) for _ in range(max_y + 1)]
            for x, y in cell_positions:
                matrix[y][x] = 1
            return matrix
    
    def from_matrix(self, matrix):
            cell_positions = []
            for y, row in enumerate(matrix):
                for x, cell in enumerate(row):
                    if cell:
                        cell_positions.append([x, y])
            return cell_positions
    
    def transpose(self, matrix):
            return list(zip(*matrix))
