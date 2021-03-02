
# Making Frappy Bird with Pygame
# Scorce https://www.youtube.com/watch?v=3ZPQI2-ciWI

import pygame
import sys
import random


pygame.init()  # initialising the pygame, like main()


screen = pygame.display.set_mode((576, 1024))  # Screen Resolution
game_background = pygame.image.load("assets/picture/background-day.png").convert()
game_background = pygame.transform.scale(game_background, (576, 1024))

while True:
    for event in pygame.event.get():  # the block for quitting and prevent initial lopping 
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    pygame.display.update()

