import pygame
from tetromino import Tetromino
from settings import SCREEN_HEIGTH, SCREEN_WIDTH, TILE_SIZE, GRID_WIDTH, GRID_HEIGHT, MAX_FPS, DIALOGUE_MENU_WIDTH, DEFEAT_ROW_NUM
from random import choice, randint

# Initialize the game
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH + DIALOGUE_MENU_WIDTH, SCREEN_HEIGTH))
pygame.display.set_caption('Tetris')
clock = pygame.time.Clock()

grid = [[0 for _ in range(GRID_WIDTH)] for _ in range(GRID_HEIGHT)] # 0 means empty cell, color name means filled cell with that color
game_background_surface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGTH))

def gen_random_tetromino():
    shape = choice(['I', 'O', 'T', 'S', 'Z', 'J', 'L'])
    shape = 'S'
    print(f"Generating a {shape} tetromino")
    color = choice(['red', 'green', 'blue', 'yellow', 'purple', 'orange', 'cyan'])
    cell_positions = []
    if shape == 'I':
        origin_point = (randint(0, GRID_WIDTH - 4), 1)
        [cell_positions.append([origin_point[0] + i, origin_point[1]]) for i in range(4)]
    elif shape == 'O':
        origin_point = (randint(0, GRID_WIDTH - 2), 0)
        [cell_positions.append([origin_point[0] + i, origin_point[1] + j]) for i in range(2) for j in range(2)]
    elif shape == 'T':
        origin_point = (randint(0, GRID_WIDTH - 3), 1)
        [cell_positions.append([origin_point[0] + i, origin_point[1] + j]) for i in range(3) for j in range(2)]
        cell_positions.append([origin_point[0] + 1, origin_point[1] + 2])
    elif shape == 'S':
        origin_point = (randint(0, GRID_WIDTH - 3), 1)
        [cell_positions.append([origin_point[0] + i, origin_point[1] + 1]) for i in range(2)]
        [cell_positions.append([origin_point[0] + i + 1, origin_point[1]]) for i in range(2)]
    elif shape == 'Z':
        origin_point = (randint(0, GRID_WIDTH - 3), 1)
        [cell_positions.append([origin_point[0] + i, origin_point[1] - 1]) for i in range(2)]
        [cell_positions.append([origin_point[0] + i + 1, origin_point[1]]) for i in range(2)]                   
    elif shape == 'J':
        origin_point = (randint(0, GRID_WIDTH - 3), 1)
        cell_positions.append([origin_point[0], origin_point[1] - 1])
        [cell_positions.append([origin_point[0] + i, origin_point[1]]) for i in range(3)]
    elif shape == 'L':
        origin_point = (randint(0, GRID_WIDTH - 3), 1)
        [cell_positions.append([origin_point[0] + i, origin_point[1]]) for i in range(3)]
        cell_positions.append([origin_point[0] + 2, origin_point[1] - 1])
        
    
    return Tetromino(screen, color, cell_positions)

current_tetromino = gen_random_tetromino()

def handle_keyboard_events(key):
    if key == pygame.K_a: current_tetromino.move_left()
    elif key == pygame.K_d: current_tetromino.move_right()
    elif key == pygame.K_q: current_tetromino.rotate_left()
    elif key == pygame.K_e: current_tetromino.rotate_right()
    #elif key == pygame.K_s: current_tetromino.move_down()

def update_game():
    global current_tetromino

    # Check if tetromino has reached loose cells
    for cell_position in current_tetromino.cell_positions:
        column = cell_position[0]
        row = cell_position[1]
        if row == GRID_HEIGHT - 1 or grid[row + 1][column] != 0: #If cells need to be converted
            for cell_position in current_tetromino.cell_positions:
                column = cell_position[0]
                row = cell_position[1]
                grid[row][column] = current_tetromino.color # Add cell to the grid

            # Create a new tetromino
            current_tetromino = gen_random_tetromino()
            break

    #Move tretramino down one cell
    current_tetromino.move_down()

def check_defeat():
    for column in range(GRID_WIDTH):
        if grid[DEFEAT_ROW_NUM][column] != 0:
            print('Game Over')
            pygame.quit()
            exit()

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

    #Update logic
    update_game()
    check_defeat()

    #Render
    screen.fill('darkgrey')
    screen.blit(game_background_surface, (0, 0))
    draw_grid() # Draw tetraminos on the grid and loose cells

    pygame.display.flip()
    clock.tick(MAX_FPS)