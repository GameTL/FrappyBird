# object are pipe, bird and ground

import pygame
import neat
import time
import random
import os
import sys

resolution_width = 576  # inital = 576
resolution_height = 1024  # inital = 1024

'''
game_background = pygame.image.load("assets/picture/background-day.png").convert()
game_background = pygame.transform.scale(game_background, (resolution_width, resolution_height)) # STRECH the wallpaper
'''


bird_imgs = [pygame.transform.scale2x(pygame.image.load("assets/picture/redbird-downflap.png")),
            pygame.transform.scale2x(pygame.image.load("assets/picture/redbird-midflap.png")),
            pygame.transform.scale2x(pygame.image.load("assets/picture/redbird-upflap.png"))]
pipe_imgs = pygame.transform.scale2x(pygame.image.load("assets/picture/pipe-green.png"))
base_imgs = pygame.transform.scale2x(pygame.image.load("assets/picture/base.png"))
background_imgs = pygame.transform.scale2x(pygame.image.load("assets/picture/background-day.png"))


class Bird():
    imgs = bird_imgs
    MAX_ROTATION = 25 # how much tilt
    ROTATION_VELOCITY = 20 
    ANIMATION_TIME = 5 # how fast the bird flap its wiong

    def __init__(self, x, y): # x&y is the starting position of the bird
        self.x = x
        self.y = y
        self.tilt = 0 # how much the bird image is tilted, inital is 0
        self.tick_count = 0
        self.velocity = 0
        self.height = self.y
        self.img_count = 0 # for keeping track of which image is showing

    def jump(self): # flap up, for pygame (0,0) is the top left of the window
        # negetive y is up and positive y is down, x direction is conventional
        self.velocity = -10.5 # jump up with a velocity of 10.5
        self.tick_count = 0
        self.height = self.y

    def move(self):
        self.tick_count += 1 # pretty much a framerate counter

        displacement = self.velocity*self.tick_count + 1.5*self.tick_count**2 # Arc displacement for fine tuning gravity here\
        if displacement >= 16:
            displacement = 16
        if displacement < 0:
            displacement -= 2

        self.y = self.y + displacement

        if displacement < 0 or self.y < self.height + 50:
            if self.tilt < self.MAX_ROTATION:
                self.tilt = self.MAX_ROTATION
        else:
            if self.tilt > -90:
                self.tilt -= self.ROTATION_VELOCITY

    def draw(self, window):
        self.img_count += 1

        if self.img_count < self.ANIMATION_TIME:
            self.imgs = self.bird_imgs[0] ####
        elif self.img_count < self.ANIMATION_TIME*2:
            self.imgs = self.bird_imgs[1] ####
        elif self.img_count < self.ANIMATION_TIME*3:
            self.imgs = self.bird_imgs[2] ####
        elif self.img_count < self.ANIMATION_TIME*2:
            self.imgs = self.bird_imgs[1] ####
        elif self.img_count < self.ANIMATION_TIME*2:
            self.imgs = self.bird_imgs[0] ####
            self.img_count = 0
        if self.tilt <= -80:
            self.imgs = self.bird_imgs[1]
            self.img_count = self.ANIMATION_TIME

        # this is for rotating the bird up and down with the centre of the image as a pivot
        rotated_image = pygame.transform.rotate(self.imgs, self.tilt)
        new_rect = rotated_image.get_rect(centre=self.bird_imgs.get_rect(topleft = (self.x,self.y)).center)
        window.blit(rotated_image, new_rect.top.left)

    def get_mask(self):
        return pygame.masl.from_surface(self.imgs)


def draw_window(window, Bird):
    window.blit(background_imgs, (0, 0))

    Bird.draw(window)
    pygame.display.update()


def main():
    bird = Bird(200, 200)  # position 200
    window = pygame.display.set_mode((resolution_width, resolution_height))
    run = True
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        draw_window(window, bird)
        pygame.display.update()


main()
