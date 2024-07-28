import pygame
from tetromino import Tetromino
from settings import *

# Initialize the game
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH + DIALOGUE_MENU_WIDTH, SCREEN_HEIGTH))
pygame.display.set_caption('Tetris')
clock = pygame.time.Clock()

grid = [[0 for _ in range(GRID_WIDTH)] for _ in range(GRID_HEIGHT)] # 0 means empty cell, color name means filled cell with that color
current_tetromino = Tetromino(screen, [[0, 0], [1, 0], [2, 0], [3, 0]], 'red')

game_background_surface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGTH))

def handle_keyboard_events(key):
    if key == pygame.K_a: current_tetromino.move_left()
    elif key == pygame.K_d: current_tetromino.move_right()
    elif key == pygame.K_q: current_tetromino.rotate_left()
    elif key == pygame.K_e: current_tetromino.rotate_right()

def update_game():
    global current_tetromino

    #Check if tetramino has reached loose cells
    for cell_position in current_tetromino.cell_positions:
        column = cell_position[0]
        row = cell_position[1]
        if row == GRID_HEIGHT - 1 or grid[row + 1][column] != 0:
            #Add tetramino to the grid
            for cell_position in current_tetromino.cell_positions:
                column = cell_position[0]
                row = cell_position[1]
                grid[row][column] = current_tetromino.color

            #Create a new tetramino
            current_tetromino = Tetromino(screen, [[0, 0], [1, 0], [2, 0], [3, 0]], 'red')
            break

    #Move tretramino down one cell
    current_tetromino.move_down()



def draw_grid():
    #Draw tetramoino's cells
    for cell_position in current_tetromino.cell_positions:
        column = cell_position[0]
        row = cell_position[1]
        pygame.draw.rect(screen, current_tetromino.color, (column * TILE_SIZE, row * TILE_SIZE, TILE_SIZE, TILE_SIZE))

    #Draw loose cells
    for row in range(GRID_HEIGHT):
        for column in range(GRID_WIDTH):
            if grid[row][column] != 0:
                pygame.draw.rect(screen, grid[row][column], (column * TILE_SIZE, row * TILE_SIZE, TILE_SIZE, TILE_SIZE))
    
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        elif event.type == pygame.KEYDOWN:
            handle_keyboard_events(event.key)

    update_game()

    screen.fill('darkgrey')
    screen.blit(game_background_surface, (0, 0))
    draw_grid() # Draw tetraminos on the grid and loose cells

    pygame.display.flip()
    clock.tick(MAX_FPS)