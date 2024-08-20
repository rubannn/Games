import pygame
import time
import random


pygame.init()


# Определяем цвета

white = (255, 255, 255)
yellow = (255, 255, 102)
black = (0, 0, 0)
red = (213, 50, 80)
green = (0, 255, 0)
blue = (50, 153, 213)


# Настройки дисплея
dis_width = 800
dis_height = 600


dis = pygame.display.set_mode((dis_width, dis_height))

pygame.display.set_caption("Snake Game")


clock = pygame.time.Clock()


snake_block = 50
snake_speed = 5

font_style = pygame.font.SysFont(None, 50)
score_font = pygame.font.SysFont(None, 35)


def your_score(score):
    value = score_font.render(f"Your Score: {score}", True, yellow)
    dis.blit(value, [0, 0])


def our_snake(snake_block, snake_list):
    for x in snake_list:
        pygame.draw.rect(dis, green, [x[0], x[1], snake_block, snake_block])


def message(msg, color):
    mesg = font_style.render(msg, True, color)
    dis.blit(mesg, [dis_width / 6, dis_height / 3])


def gameLoop():
    game_over = False
    game_close = False
    x1 = dis_width / 2
    y1 = dis_height / 2

    x1_change = 0
    y1_change = 0

    snake_list = []
    length_of_snake = 1

    xy = snake_block * 1.0
    foodx = round(random.randrange(0, dis_width - snake_block) / xy) * xy
    foody = round(random.randrange(0, dis_height - snake_block) / xy) * xy

    while not game_over:
        while game_close:
            dis.fill(blue)
            message("You Lost! Press C-Play Again or Q-Quit", red)
            your_score(length_of_snake - 1)
            pygame.display.update()
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        game_over = True
                        game_close = False

                    if event.key == pygame.K_c:
                        gameLoop()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    x1_change = -snake_block
                    y1_change = 0
                elif event.key == pygame.K_RIGHT:
                    x1_change = snake_block
                    y1_change = 0
                elif event.key == pygame.K_UP:
                    y1_change = -snake_block
                    x1_change = 0
                elif event.key == pygame.K_DOWN:
                    y1_change = snake_block
                    x1_change = 0

        if x1 >= dis_width or x1 < 0 or y1 >= dis_height or y1 < 0:
            game_close = True

        x1 += x1_change
        y1 += y1_change
        dis.fill(black)

        pygame.draw.rect(dis, white, [foodx, foody, snake_block, snake_block])

        snake_head = []
        snake_head.append(x1)
        snake_head.append(y1)

        snake_list.append(snake_head)
        if len(snake_list) > length_of_snake:
            del snake_list[0]

        for x in snake_list[:-1]:
            if x == snake_head:
                game_close = True

        our_snake(snake_block, snake_list)
        your_score(length_of_snake - 1)
        pygame.display.update()

        if x1 == foodx and y1 == foody:
            xy = snake_block * 1.0
            foodx = round(random.randrange(0, dis_width - snake_block) / xy) * xy
            foody = round(random.randrange(0, dis_height - snake_block) / xy) * xy
            length_of_snake += 1
        clock.tick(snake_speed)

    pygame.quit()
    quit()


gameLoop()
