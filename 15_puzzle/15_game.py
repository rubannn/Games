import pygame
import random
import sys

# Инициализация Pygame
pygame.init()

BORDER_SIZE = 4

# Определение параметров окна
WIDTH = 400
HEIGHT = 400
CELL_SIZE = WIDTH // BORDER_SIZE

# Определение цветов
COLOR_TEXT = (65, 105, 225)
COLOR_BLOCK = (200, 200, 200)
COLOR_FILL = (255, 255, 255)

# Радиус круглого угла фишки
RADIUS = 20
FONT_SIZE = 70

# Создание окна
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Игра 15")


# Функция для проверки четности перестаноки, т.е. проверка существования решения
def is_can_solved(lst):
    sol = 0
    for i in range(BORDER_SIZE**2):
        if lst[i]:
            for j in range(i):
                if lst[j] > lst[i]:
                    sol += 1
    sol += lst.index(0) // BORDER_SIZE + 1
    return sol % 2 == (BORDER_SIZE**2) % 2


# Функция для создания и перемешивания пятнашек
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


# Функция для нахождения пустой ячейки
def find_empty_cell(board):
    for i in range(BORDER_SIZE):
        for j in range(BORDER_SIZE):
            if board[i][j] == 0:
                return i, j


# Функция для проверки завершения игры
def check_win(board):
    k = 1
    for i in range(BORDER_SIZE):
        for j in range(BORDER_SIZE):
            if board[i][j] != k % BORDER_SIZE**2:
                return False
            k += 1
    return True


# Функция для обмена пятнашки с пустой ячейкой
def swap(board, row1, col1, row2, col2):
    board[row1][col1], board[row2][col2] = board[row2][col2], board[row1][col1]


def condition(a, b, mode):
    return [a >= b, a <= b][mode]


# refactor ...line 110-124
def move_empty_cell(board, row, col, empty_row, empty_col, type):
    pass


# Основная функция игры
def main():
    # Создание игрового поля
    board = create_board()
    empty_row, empty_col = find_empty_cell(board)

    while True:
        # Обработка событий
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
                        mode = col > empty_col
                        x, y = empty_row, empty_col + (-1) ** (mode + 1)
                        while condition(y, col, mode):
                            swap(board, x, y, empty_row, empty_col)
                            empty_row, empty_col = x, y
                            x, y = empty_row, empty_col + (-1) ** (mode + 1)
                    elif col == empty_col:
                        mode = row > empty_row
                        x, y = empty_row + (-1) ** (mode + 1), empty_col
                        while condition(x, row, mode):
                            swap(board, x, y, empty_row, empty_col)
                            empty_row, empty_col = x, y
                            x, y = empty_row + (-1) ** (mode + 1), empty_col

        # Отрисовка игрового поля
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

        # Проверка завершения игры
        if check_win(board):
            font = pygame.font.Font(None, FONT_SIZE)
            text = font.render("Вы выиграли!", True, COLOR_BLOCK)
            text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
            screen.blit(text, text_rect)

        pygame.display.flip()


if __name__ == "__main__":
    main()
