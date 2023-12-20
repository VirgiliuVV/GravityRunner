import random

import pygame


class Obstacle:
    def __init__(self, typeOfEnemy, speed):
        self.rect = pygame.image.load('img/enemy/barrel.png').get_rect()
        self.rect.x = 800

        gravity = random.choice(['up', 'down'])

        if gravity == 'down':
            if typeOfEnemy == 'barrel':
                self.image = pygame.image.load('img/enemy/barrel.png')
                self.rect.y = 363
            elif typeOfEnemy == 'double_barrel':
                self.image = pygame.image.load('img/enemy/double_barrel.png')
                self.rect.y = 330
            else:
                self.image = pygame.image.load('img/enemy/Lava.png')
                self.rect.y = 404
        else:
            if typeOfEnemy == 'barrel':
                self.image = pygame.image.load('img/enemy/reversed_barrel.png')
                self.rect.y = 123
            elif typeOfEnemy == 'double_barrel':
                self.image = pygame.image.load('img/enemy/reversed_double_barrel.png')
                self.rect.y = 123
            else:
                self.image = pygame.image.load('img/enemy/Lava.png')
                self.rect.y = 404
        self.speed = speed

    def move(self):
        self.rect.x -= self.speed

    def draw(self, screen):
        screen.blit(self.image, self.rect)
