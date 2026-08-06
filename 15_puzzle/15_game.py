import pygame
import random
import sys

# Initialize Pygame
pygame.init()

BORDER_SIZE = 4
FONT_SIZE = {3: 80, 4: 70, 5: 60, 6: 50, 7: 40, 8: 30}.get(BORDER_SIZE, 50)

# Window parameters
WIDTH = 400
HEIGHT = 400
CELL_SIZE = WIDTH // BORDER_SIZE

# Colors
COLOR_TEXT = (65, 105, 225)
COLOR_BLOCK = (200, 200, 200)
COLOR_FILL = (255, 255, 255)

# Rounded tile corner radius
RADIUS = 20

# Create window
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("15 Puzzle")


# Function to check parity of the permutation, i.e. whether a solution exists
def is_can_solved(lst):
    sol = 0
    for i in range(BORDER_SIZE**2):
        if lst[i]:
            for j in range(i):
                if lst[j] > lst[i]:
                    sol += 1
    sol += lst.index(0) // BORDER_SIZE + 1
    return sol % 2 == (BORDER_SIZE**2) % 2


# Function to create and shuffle the 15-puzzle board
def create_board():
    board = [[0] * BORDER_SIZE for _ in range(BORDER_SIZE)]
    numbers = list(range(BORDER_SIZE**2))
    random.shuffle(numbers)
    while not is_can_solved(numbers):
        random.shuffle(numbers)
    k = 0
    for i in range(BORDER_SIZE):
        for j in range(BORDER_SIZE):
            board[i][j] = numbers[k]
            k += 1
    return board


# Function to locate the empty cell
def find_empty_cell(board):
    for i in range(BORDER_SIZE):
        for j in range(BORDER_SIZE):
            if board[i][j] == 0:
                return i, j


# Function to check if the game is finished
def check_win(board):
    k = 1
    for i in range(BORDER_SIZE):
        for j in range(BORDER_SIZE):
            if board[i][j] != k % BORDER_SIZE**2:
                return False
            k += 1
    return True


# Function to swap a tile with the empty cell
def swap(board, row1, col1, row2, col2):
    board[row1][col1], board[row2][col2] = board[row2][col2], board[row1][col1]


def condition(p1, p2, pair, mode):
    a, b = [p2, p1][pair]
    return [a >= b, a <= b][mode]


# refactor ...line 110-124
def move_cells():
    pass


# Main game function
def main():
    # Create the game board
    board = create_board()
    empty_row, empty_col = find_empty_cell(board)
    vec = (-1, 1)

    while True:
        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = pygame.mouse.get_pos()
                col = x // CELL_SIZE
                row = y // CELL_SIZE
                if abs(row - empty_row) + abs(col - empty_col) == 1:
                    swap(board, row, col, empty_row, empty_col)
                    empty_row, empty_col = row, col
                # смещение строки/столбца целиком в зависимости от положения пустой клетки
                elif abs(row - empty_row) * abs(col - empty_col) == 0:
                    if row == empty_row:
                        k1, k2, pair = (0, 1, 0)
                        mode = col > empty_col
                    elif col == empty_col:
                        k1, k2, pair = (1, 0, 1)
                        mode = row > empty_row

                    x, y = empty_row + k1 * vec[mode], empty_col + k2 * vec[mode]
                    while condition((x, row), (y, col), pair, mode):
                        swap(board, x, y, empty_row, empty_col)
                        empty_row, empty_col = x, y
                        x, y = empty_row + k1 * vec[mode], empty_col + k2 * vec[mode]

        # Draw the game board
        screen.fill(COLOR_FILL)
        for i in range(BORDER_SIZE):
            for j in range(BORDER_SIZE):
                if board[i][j] != 0:
                    pygame.draw.rect(
                        screen,
                        COLOR_BLOCK,
                        (j * CELL_SIZE, i * CELL_SIZE, CELL_SIZE, CELL_SIZE),
                        1,
                        RADIUS,
                    )
                    font = pygame.font.Font(None, FONT_SIZE)
                    text = font.render(str(board[i][j]), True, COLOR_TEXT)
                    text_rect = text.get_rect(
                        center=(
                            j * CELL_SIZE + CELL_SIZE // 2,
                            i * CELL_SIZE + CELL_SIZE // 2,
                        )
                    )
                    screen.blit(text, text_rect)

        # Check if the game is finished
        if check_win(board):
            font = pygame.font.Font(None, FONT_SIZE)
            text = font.render("You won!", True, COLOR_BLOCK)
            text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
            screen.blit(text, text_rect)

        pygame.display.flip()


if __name__ == "__main__":
    main()
