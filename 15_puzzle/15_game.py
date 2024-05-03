import pygame
import random
import sys

# Инициализация Pygame
pygame.init()

# Определение цветов
COLOR_TEXT = (65, 105, 225)
COLOR_BLOCK = (200, 200, 200)
COLOR_FILL = (255, 255, 255)

# Определение параметров окна
WIDTH = 400
HEIGHT = 400
CELL_SIZE = WIDTH // 4

# Радиус круглого угла фишки
RADIUS = 20
FONT_SIZE = 70

# Создание окна
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Игра 15")


# Функция для проверки четности перестаноки, т.е. проверка существования решения
def is_can_solved(lst):
    sol, n = 0, len(lst)
    for i in range(n):
        if lst[i]:
            for j in range(i):
                if lst[j] > lst[i]:
                    sol += 1
    sol += lst.index(0) // 4 + 1
    return sol % 2 == 0


# Функция для создания и перемешивания пятнашек
def create_board():
    board = [[0] * 4 for _ in range(4)]
    numbers = list(range(16))
    random.shuffle(numbers)
    while not is_can_solved(numbers):
        random.shuffle(numbers)
    k = 0
    for i in range(4):
        for j in range(4):
            board[i][j] = numbers[k]
            k += 1
    return board


# Функция для нахождения пустой ячейки
def find_empty_cell(board):
    for i in range(4):
        for j in range(4):
            if board[i][j] == 0:
                return i, j


# Функция для проверки завершения игры
def check_win(board):
    k = 1
    for i in range(4):
        for j in range(4):
            if board[i][j] != k % 16:
                return False
            k += 1
    return True


# Функция для обмена пятнашки с пустой ячейкой
def swap(board, row1, col1, row2, col2):
    board[row1][col1], board[row2][col2] = board[row2][col2], board[row1][col1]


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

        # Отрисовка игрового поля
        screen.fill(COLOR_FILL)
        for i in range(4):
            for j in range(4):
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
            font = pygame.font.Font(None, 48)
            text = font.render("Вы выиграли!", True, COLOR_BLOCK)
            text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
            screen.blit(text, text_rect)

        pygame.display.flip()


if __name__ == "__main__":
    main()
