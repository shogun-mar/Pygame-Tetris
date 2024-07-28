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

tetrominoes = [gen_random_tetromino() for _ in range(4)]
current_tetromino = tetrominoes[0]

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
        if row == GRID_HEIGHT - 1 or (row + 1 < len(grid) and grid[row + 1][column] != 0): #If cells need to be converted
            for cell_position in current_tetromino.cell_positions:
                column = cell_position[0]
                row = cell_position[1]
                grid[row][column] = current_tetromino.color # Add cell to the grid

            # Create a new tetromino
            tetrominoes.append(gen_random_tetromino())
            current_tetromino = tetrominoes[0]
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
    
def draw_dialogue_menu():
    # Offsets
    tetramino_offset = [50, 0]
    cell_offset = [0, 0]

    # Draw tetraminoes on the dialogue menu, excluding the first element
    for tetromino in tetrominoes[1:]:
        tetramino_offset[1] += 100  # Increment vertical offset for each tetromino
        cell_offset = [0, 0]  # Reset cell offset for each tetromino
        for i in range(len(tetromino.cell_positions)):
            current_column = tetromino.cell_positions[i][0]
            current_row = tetromino.cell_positions[i][1]
            if i > 0:
                previous_column = tetromino.cell_positions[i-1][0]
                previous_row = tetromino.cell_positions[i-1][1]
                if current_column == previous_column + 1:
                    cell_offset[0] += TILE_SIZE
                if current_row == previous_row + 1:
                    cell_offset[1] += TILE_SIZE

            x = SCREEN_WIDTH + tetramino_offset[0] + cell_offset[0]
            y = tetramino_offset[1] + cell_offset[1]
            pygame.draw.rect(screen, tetromino.color, (x, y, TILE_SIZE, TILE_SIZE))

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
    draw_dialogue_menu()

    pygame.display.flip()
    clock.tick(MAX_FPS)