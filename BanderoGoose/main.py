import random
import os

import pygame
from pygame.constants import QUIT, K_DOWN, K_UP, K_LEFT, K_RIGHT

pygame.init()

FPS = pygame.time.Clock()
HEIGHT = 800
WIDTH = 1200

FONT = pygame.font.SysFont("Verdana", 20)

COLOR_WHITE = (255, 255, 255)
COLOR_BLACK = (0, 0, 0)
COLOR_BLUE = (0, 0, 255)
COLOR_RED = (255, 0, 0)

main_display = pygame.display.set_mode((WIDTH, HEIGHT))
dir_path = os.path.dirname(os.path.abspath(__file__))
bg = pygame.transform.scale(
    pygame.image.load(f"{dir_path}/img/background.png"), (WIDTH, HEIGHT)
)
bg_x1 = 0
bg_x2 = bg.get_width()
bg_move = 3

IMG_PATH = f"{dir_path}/img/goose"
PLAYER_IMGS = os.listdir(IMG_PATH)

player_size = (75, 50)
player = pygame.image.load(f"{dir_path}/img/player.png").convert_alpha()
# pygame.Surface(player_size)
# player.fill(COLOR_WHITE)
player_rect = player.get_rect()
player_speed = 4
player_move_down = [0, player_speed]
player_move_right = [player_speed, 0]
player_move_left = [-player_speed, 0]
player_move_up = [0, -player_speed]

enemy_img = pygame.image.load(f"{dir_path}/img/enemy.png").convert_alpha()
bonus_img = pygame.image.load(f"{dir_path}/img/bonus.png").convert_alpha()


def create_enemy():
    enemy_size = (75, 25)
    enemy = pygame.transform.scale(enemy_img, enemy_size)
    enemy_rect = pygame.Rect(
        WIDTH, random.randint(0 + enemy_size[0], HEIGHT - enemy_size[0]), *enemy_size
    )
    enemy_move = [random.randint(-8, -4), 0]
    return [enemy, enemy_rect, enemy_move]


def create_bonus():
    bonus_size = (75, 75)
    bonus = pygame.transform.scale(bonus_img, bonus_size)
    bonus_rect = pygame.Rect(
        random.randint(0 + bonus_size[1], WIDTH - bonus_size[1]), 0, *bonus_size
    )
    bonus_move = [0, random.randint(4, 8)]
    return [bonus, bonus_rect, bonus_move]


CREATE_ENEMY = pygame.USEREVENT + 1
pygame.time.set_timer(CREATE_ENEMY, 1500)

CREATE_BONUS = pygame.USEREVENT + 2
pygame.time.set_timer(CREATE_BONUS, 3000)
CHANGE_IMG = pygame.USEREVENT + 3
pygame.time.set_timer(CHANGE_IMG, 200)

enemies = []
bonuses = []
score = 0
img_index = 0


playing = True
while playing:
    FPS.tick(120)
    for event in pygame.event.get():
        if event.type == QUIT:
            playing = False
        if event.type == CREATE_ENEMY:
            enemies.append(create_enemy())
        if event.type == CREATE_BONUS:
            bonuses.append(create_bonus())
        if event.type == CHANGE_IMG:
            player = pygame.transform.scale(
                pygame.image.load(os.path.join(IMG_PATH, PLAYER_IMGS[img_index])),
                player_size,
            )
            img_index = (img_index + 1) % len(PLAYER_IMGS)

    bg_x1 -= bg_move
    bg_x2 -= bg_move
    if bg_x1 < -bg.get_width():
        bg_x1 = bg.get_width()

    if bg_x2 < -bg.get_width():
        bg_x2 = bg.get_width()

    main_display.blit(bg, (bg_x1, 0))
    main_display.blit(bg, (bg_x2, 0))

    keys = pygame.key.get_pressed()

    if keys[K_DOWN] and player_rect.bottom < HEIGHT:
        player_rect = player_rect.move(player_move_down)

    if keys[K_RIGHT] and player_rect.right < WIDTH:
        player_rect = player_rect.move(player_move_right)

    if keys[K_LEFT] and player_rect.left > 0:
        player_rect = player_rect.move(player_move_left)

    if keys[K_UP] and player_rect.top > 0:
        player_rect = player_rect.move(player_move_up)

    for enemy in enemies:
        enemy[1] = enemy[1].move(enemy[2])
        main_display.blit(enemy[0], enemy[1])

        if player_rect.colliderect(enemy[1]):
            playing = False

    for bonus in bonuses:
        bonus[1] = bonus[1].move(bonus[2])
        main_display.blit(bonus[0], bonus[1])

        if player_rect.colliderect(bonus[1]):
            score += 1
            bonuses.pop(bonuses.index(bonus))

    main_display.blit(FONT.render(str(score), True, COLOR_BLACK), (WIDTH - 50, 20))
    main_display.blit(player, player_rect)

    pygame.display.flip()
    for enemy in enemies:
        if enemy[1].left < 0:
            enemies.pop(enemies.index(enemy))
    for bonus in bonuses:
        if bonus[1].bottom > HEIGHT:
            bonuses.pop(bonuses.index(bonus))
    # print(f'{len(enemies)=}  {len(bonuses)=}')
