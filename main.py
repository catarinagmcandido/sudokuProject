import pygame

# This list represents the sudoku grid, every 0 represents an empty space
sudoku_grid = [[0, 0, 0, 0, 0, 0, 0, 0, 0],
               [0, 0, 0, 0, 4, 0, 0, 0, 0],
               [0, 0, 0, 8, 0, 7, 0, 0, 0],
               [0, 0, 7, 0, 0, 0, 2, 0, 0],
               [0, 5, 0, 0, 0, 0, 0, 7, 0],
               [0, 0, 3, 0, 0, 0, 8, 0, 0],
               [0, 0, 0, 7, 0, 3, 0, 0, 0],
               [0, 0, 0, 0, 1, 0, 0, 0, 0],
               [0, 0, 0, 0, 0, 0, 0, 0, 0]]

# This list is to compare with the other grid, so that we know where are the default values
initial_sudoku_grid = [[0, 0, 0, 0, 0, 0, 0, 0, 0],
                       [0, 0, 0, 0, 4, 0, 0, 0, 0],
                       [0, 0, 0, 8, 0, 7, 0, 0, 0],
                       [0, 0, 7, 0, 0, 0, 2, 0, 0],
                       [0, 5, 0, 0, 0, 0, 0, 7, 0],
                       [0, 0, 3, 0, 0, 0, 8, 0, 0],
                       [0, 0, 0, 7, 0, 3, 0, 0, 0],
                       [0, 0, 0, 0, 1, 0, 0, 0, 0],
                       [0, 0, 0, 0, 0, 0, 0, 0, 0]]

# This tuple represents the 4 lateral sums of the frameless variant
# lateral_sums[0]= left sums; lateral_sums[1]= above sums; lateral_sums[2]= bottom sums; lateral_sums[3]= right sums;
lateral_sums = ([10, 5, 12, 5, 13, 9, 18, 13, 9],
                [14, 17, 9, 11, 2, 10, 9, 10, 9, 11],
                [9, 11, 2, 9, 9, 9, 21, 9, 9],
                [12, 12, 14, 6, 14, 6, 14, 11, 14]
                )

background = pygame.image.load('images/background_image.jpg')
width = 650
cell_size = 650 / 12

# Set the size of the window and the background color
screen = pygame.display.set_mode((width, width))
screen.blit(background, (0, 0))

# Traditional Japanese Music - Koto & Shakuhachi Lullaby
pygame.mixer.init()
pygame.mixer.music.load('soundtrack/sound.wav')
pygame.mixer.music.play(-1)

# Set the name and icon of the window
pygame.display.set_caption('Sudoku Frameless')
gameIcon = pygame.image.load('images/8biticon.jpg')
pygame.display.set_icon(gameIcon)

# Change the cursor
pygame.mouse.set_cursor(pygame.cursors.tri_left)

# Render the window
pygame.display.flip()

running_game = True
mouse_position = ()

pygame.font.init()
font = pygame.font.SysFont('arial', 30)


# Function to insert the numbers in a certain position
def insert_numbers(value, x_pos, y_pos):
    # We need to subtract -2 to get the correct index of the lists, because the positions begins outside the grid
    # Ex: the first cell of the grid has the position [2][2] so we need do take -2 to get the real position [0][0]
    if initial_sudoku_grid[y_pos - 2][x_pos - 2] != sudoku_grid[y_pos - 2][x_pos - 2] or initial_sudoku_grid[y_pos - 2][
        x_pos - 2] == 0:
        sudoku_grid[y_pos - 2][x_pos - 2] = int(value)
        constructor_grid(sudoku_grid, lateral_sums)
        if is_valid_move(sudoku_grid) != '':
            text = is_valid_move(sudoku_grid)
            pygame.display.flip()
            validation_message = font.render(text, True, (240, 21, 21))
            screen.blit(validation_message, (80, 15))
    else:
        validation_message = font.render('You are trying to change a default number', True, (240, 21, 21))
        screen.blit(validation_message, (80, 15))


def constructor_grid(sudoku_grid, lateral_sums):
    screen.blit(background, (0, 0))
    pygame.display.flip()
    for i in range(0, 10):
        if i % 3 == 0:
            pygame.draw.line(screen, (0, 0, 0), (100 + 50 * i, 100), (100 + 50 * i, 550), 5)
            pygame.draw.line(screen, (0, 0, 0), (100, 100 + 50 * i), (550, 100 + 50 * i), 5)
        pygame.draw.line(screen, (0, 0, 0), (100 + 50 * i, 100), (100 + 50 * i, 550), 1)
        pygame.draw.line(screen, (0, 0, 0), (100, 100 + 50 * i), (550, 100 + 50 * i), 1)

    for i in range(0, len(sudoku_grid[0])):
        for j in range(0, len(sudoku_grid[0])):
            if 0 < sudoku_grid[i][j] < 10:
                value = sudoku_grid[i][j]
                blit_number = font.render(str(value), True, (0, 0, 0))
                screen.blit(blit_number, ((j + 1) * 50 + 60, (i + 2) * 50))
    for i in range(0, 9):
        value = lateral_sums[0][i]
        blit_number = font.render(str(value), True, (0, 0, 0))
        screen.blit(blit_number, ((i + 1) + 60, (i + 1) * 50 + 60))

    for i in range(0, 9):
        value = lateral_sums[1][i]
        blit_number = font.render(str(value), True, (0, 0, 0))
        screen.blit(blit_number, ((i + 1) * 50 + 60, (i + 1) + 50))

    for i in range(0, 9):
        value = lateral_sums[3][i]
        blit_number = font.render(str(value), True, (0, 0, 0))
        screen.blit(blit_number, ((i + 1) + 560, (i + 1) * 50 + 50))

    for i in range(0, 9):
        value = lateral_sums[2][i]
        blit_number = font.render(str(value), True, (0, 0, 0))
        screen.blit(blit_number, ((i + 1) * 50 + 60, (i + 1) + 550))

    return pygame.display.update()


def fill_cell_selected(x_cell, y_cell):
    if 50 < x_cell <= 500 and 50 < y_cell <= 500:
        constructor_grid(sudoku_grid, lateral_sums)
        pygame.draw.rect(screen, color, (x_cell, y_cell, 50, 50), 5)


# This function handles all the incorrect moves
def is_valid_move(sudoku_grid):
    return has_duplicated_numbers_columns(sudoku_grid) \
           or has_duplicated_numbers_rows(sudoku_grid) \
           or has_duplicated_numbers_matrix(sudoku_grid)


# Search for duplicated values in rows
def has_duplicated_numbers_rows(sudoku_grid):
    for row in sudoku_grid:
        for row_element in row:
            if row_element != 0 and row.count(row_element) > 1:
                return 'You have duplicated values in the same row'


# Search for duplicated values in columns
def has_duplicated_numbers_columns(sudoku_grid):
    save_col_items = []
    for x in range(8):
        save_col_items.clear()
        for y in range(8):
            if sudoku_grid[y][x] != 0:
                save_col_items.append(sudoku_grid[y][x])
                if save_col_items.count(sudoku_grid[y][x]) > 1:
                    return 'You have duplicated values in the same column'


# Search for duplicated values in sub-matrix 3x3
def has_duplicated_numbers_matrix(sudoku_grid):
    saved_items = []

    for row in range(0, 9, 3):
        for col in range(0, 9, 3):
            saved_items.clear()
            for x in range(row, row + 3):
                for y in range(col, col + 3):
                    if sudoku_grid[x][y] != 0:
                        saved_items.append(sudoku_grid[x][y])
                        if saved_items.count(sudoku_grid[x][y]) > 1:
                            return 'You have duplicated values inside the matrix 3x3'


constructor_grid(sudoku_grid, lateral_sums)

# Loop for the time the game is running
while running_game:

    pygame.display.flip()
    mouse_pressed = pygame.mouse.get_pressed()

    for event in pygame.event.get():

        # The mouse_pressed is a tuple with 3 elements, the first one says if it was clicked or not
        if mouse_pressed[0] == 1:
            color = (249, 12, 225)
            mouse_pos = pygame.mouse.get_pos()
            y_pos = mouse_pos[1] / cell_size
            x_pos = mouse_pos[0] / cell_size
            x_cell = round(mouse_pos[0] / cell_size) * 50
            y_cell = round(mouse_pos[1] / cell_size) * 50
            clicked = True

            # To highlight the selected cell
            fill_cell_selected(x_cell, y_cell)

        # After clicking in a position, user presses a key to put in that place
        if event.type == pygame.KEYDOWN:
            number_pressed = pygame.key.name(event.key)

            # This condition is to check if user is not clicking outside the grid and if it entered a number
            if number_pressed.isdigit() and 1 < int(x_pos) <= 9 and 1 < int(y_pos) <= 9:
                insert_numbers(number_pressed, round(x_pos), round(y_pos))
                clicked = False

    # When player clicks in the x to quit the game
    if event.type == pygame.QUIT:
        running_game = False
