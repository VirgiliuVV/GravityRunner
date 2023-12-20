import random
import sys
import pygame
import json

from globalSettings import *
from enemy import Obstacle
from menu import Menu
from selectCharacter import ExportCharacter

with open('score.json', 'r') as file:
    dataJson = json.load(file)


def apply_gravity():
    global currentPosition, gravity, orientation

    if gravity == 'down':
        if currentPosition != currentLimit:
            currentPosition += STG_gravity
            orientation = 0
    elif gravity == 'up':
        if currentPosition != currentLimit:
            currentPosition -= STG_gravity
            orientation = 1


def is_mouse_over_button(mouse_pos, button_pos, button_size):
    return (
            button_pos[0] <= mouse_pos[0] <= button_pos[0] + button_size[0] and
            button_pos[1] <= mouse_pos[1] <= button_pos[1] + button_size[1]
    )


# init game
pygame.init()
clock = pygame.time.Clock()
screen = pygame.display.set_mode((
    800,
    600
), flags=pygame.NOFRAME)

sound = pygame.mixer.Sound("sounds/ambient.mp3")
sound.set_volume(STG_sound)
sound.play()

Menu(screen)
while True:
    character = ExportCharacter(screen)

    if character.selectedCharacter == 'Alien':

        currentCharacter = [
            [
                pygame.image.load('img/player/alien/down/Alien1.png'),
                pygame.image.load('img/player/alien/down/Alien2.png'),
                pygame.image.load('img/player/alien/down/Alien3.png'),
                pygame.image.load('img/player/alien/down/Alien4.png'),
                pygame.image.load('img/player/alien/down/Alien5.png'),
                pygame.image.load('img/player/alien/down/Alien6.png')
            ],
            [
                pygame.image.load('img/player/alien/up/Alien1.png'),
                pygame.image.load('img/player/alien/up/Alien2.png'),
                pygame.image.load('img/player/alien/up/Alien3.png'),
                pygame.image.load('img/player/alien/up/Alien4.png'),
                pygame.image.load('img/player/alien/up/Alien5.png'),
                pygame.image.load('img/player/alien/up/Alien6.png')
            ]
        ]
    else:
        currentCharacter = [
            [
                pygame.image.load('img/player/astronaut/down/astronaut1.png'),
                pygame.image.load('img/player/astronaut/down/astronaut2.png'),
                pygame.image.load('img/player/astronaut/down/astronaut3.png'),
                pygame.image.load('img/player/astronaut/down/astronaut4.png'),
                pygame.image.load('img/player/astronaut/down/astronaut5.png'),
                pygame.image.load('img/player/astronaut/down/astronaut6.png')
            ],
            [
                pygame.image.load('img/player/astronaut/up/astronaut1.png'),
                pygame.image.load('img/player/astronaut/up/astronaut2.png'),
                pygame.image.load('img/player/astronaut/up/astronaut3.png'),
                pygame.image.load('img/player/astronaut/up/astronaut4.png'),
                pygame.image.load('img/player/astronaut/up/astronaut5.png'),
                pygame.image.load('img/player/astronaut/up/astronaut6.png')
            ]
        ]

    font = pygame.font.Font(None, 32)
    highScore = font.render('HighScore:' + str(dataJson['highScore']), True, STG_textColor)
    attempt = font.render('Attempt:' + str(dataJson['attempt']), True, STG_textColor)

    barrel_image = pygame.image.load('img/enemy/barrel.png')
    double_barrel_image = pygame.image.load('img/enemy/double_barrel.png')
    lava_pool_image = pygame.image.load('img/enemy/Lava.png')
    obstacles = []
    obstacle_spawn_timer = 0
    spawn_interval = STG_spawnObstacleInterval
    score = 0

    background = pygame.image.load('img/game/background.png')
    background_x = 0
    animationCount = 0
    running = True
    gravity = 'down'
    orientation = 0
    currentLimit = STG_bottomLimit
    currentPosition = STG_bottomLimit
    dataJson['attempt'] = dataJson['attempt'] + 1
    speed = STG_obstacleSpeed

    while running:

        with open('score.json', 'w') as file:
            json.dump(dataJson, file, indent=4)
        screen.blit(background, (background_x, 0))
        screen.blit(background, (background_x + 800, 0))

        currentScore = font.render('Score: ' + str(score), True, STG_textColor)
        screen.blit(currentScore, (20, 20))
        screen.blit(highScore, (200, 20))
        screen.blit(attempt, (450, 20))

        screen.blit(currentCharacter[orientation][animationCount], (100, currentPosition))
        animationCount += 1
        if animationCount == 6:
            animationCount = 0

        background_x -= speed
        if background_x <= -800:
            background_x = 0

        apply_gravity()

        score += 1
        if score % 400 == 0:
            speed += 5
            spawn_interval -= 1
        if spawn_interval <= 10:
            spawn_interval = 10
        obstacle_spawn_timer += 1
        if obstacle_spawn_timer == spawn_interval:
            obstacle_type = random.choice([barrel_image, double_barrel_image, lava_pool_image])
            if obstacle_type == barrel_image:
                obstacles.append(Obstacle('barrel', speed))
            elif obstacle_type == double_barrel_image:
                obstacles.append(Obstacle('double_barrel', speed))
            else:
                obstacles.append(Obstacle('lava', speed))
            obstacle_spawn_timer = 0

        for obstacle in obstacles:
            obstacle.move()
            obstacle.draw(screen)

        obstacles = [obstacle for obstacle in obstacles if obstacle.rect.x + 300 + obstacle.rect.width > 0]

        player_mask = pygame.mask.from_surface(currentCharacter[orientation][animationCount])
        player_rect = currentCharacter[orientation][animationCount].get_rect(topleft=(100, currentPosition))

        for obstacle in obstacles:
            obstacle_mask = pygame.mask.from_surface(obstacle.image)
            obstacle_rect = obstacle.image.get_rect(topleft=(obstacle.rect.x, obstacle.rect.y))

            if player_mask.overlap(obstacle_mask, (obstacle_rect.x - player_rect.x, obstacle_rect.y - player_rect.y)):
                running = False
                break
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                break
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                    break
                elif event.key == pygame.K_SPACE:
                    if gravity == 'down':
                        currentLimit = STG_topLimit
                        gravity = 'up'
                    else:
                        currentLimit = STG_bottomLimit
                        gravity = 'down'

        clock.tick(25)

    fade_surface = pygame.Surface((800, 600))
    endImage = pygame.image.load('img/game/you died.png')
    play_again = pygame.image.load('img/game/Play-again.png')
    play_again.set_alpha(0)
    endImage.set_alpha(0)

    if score > dataJson['highScore']:
        dataJson['highScore'] = score
        json.dump(dataJson, open('score.json', 'w'), indent=4)
    for alpha in range(0, 255, 10):
        endImage.set_alpha(alpha)
        screen.fill((0, 0, 0))
        screen.blit(endImage, ((800 - endImage.get_width()) / 2, (600 - endImage.get_height()) / 2))
        pygame.display.update()
        pygame.time.delay(50)

    for alpha in range(0, 255, 10):
        play_again.set_alpha(alpha)
        screen.blit(play_again, ((800 - play_again.get_width()) / 2, (900 - play_again.get_height()) / 2))
        pygame.display.update()
        pygame.time.delay(50)

    end = True
    while end:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                running = False
                pygame.quit()
                break
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if is_mouse_over_button(mouse_pos,
                                        ((800 - play_again.get_width()) / 2, (900 - play_again.get_height()) / 2),
                                        play_again.get_size()):
                    end = False

pygame.quit()
sys.exit()
