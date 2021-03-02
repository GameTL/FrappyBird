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
window = pygame.display.set_mode((resolution_width, resolution_height))
background_imgs = pygame.transform.scale(pygame.image.load(os.path.join("imgs","bg.png")).convert_alpha(), (600, 900))
bird_imgs = [pygame.transform.scale2x(pygame.image.load(os.path.join("imgs","bird" + str(x) + ".png"))) for x in range(1,4)]
base_img = pygame.transform.scale2x(pygame.image.load(os.path.join("imgs","base.png")).convert_alpha())


class Bird():
    
    IMGS = bird_imgs
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
        """
        make the bird move
        :return: None
        """
        self.tick_count += 1

        # for downward acceleration
        displacement = self.velocity*(self.tick_count) + 0.5*(3)*(self.tick_count)**2  # calculate displacement

        # terminal velocity
        if displacement >= 16:
            displacement = (displacement/abs(displacement)) * 16

        if displacement < 0:
            displacement -= 2

        self.y = self.y + displacement

        if displacement < 0 or self.y < self.height + 50:  # tilt up
            if self.tilt < self.MAX_ROTATION:
                self.tilt = self.MAX_ROTATION
        else:  # tilt down
            if self.tilt > -90:
                self.tilt -= self.ROTATION_VELOCITY

    def draw(self, window):
        self.img_count += 1

        if self.img_count <= self.ANIMATION_TIME:
            self.img = self.IMGS[0]
        elif self.img_count <= self.ANIMATION_TIME*2:
            self.img = self.IMGS[1]
        elif self.img_count <= self.ANIMATION_TIME*3:
            self.img = self.IMGS[2]
        elif self.img_count <= self.ANIMATION_TIME*4:
            self.img = self.IMGS[1]
        elif self.img_count == self.ANIMATION_TIME*4 + 1:
            self.img = self.IMGS[0]
            self.img_count = 0

        # so when bird is nose diving it isn't flapping
        if self.tilt <= -80:
            self.img = self.IMGS[1]
            self.img_count = self.ANIMATION_TIME*2
        # For animation of bird, loop through three images
        
        # this is for rotating the bird up and down with the centre of the image as a pivot
        #rotated_image = pygame.transform.rotate(self.imgs, self.tilt)
        #new_rect = rotated_image.get_rect(centre=self.bird_imgs.get_rect(topleft = (self.x,self.y)).center)
        #window.blit(rotated_image, new_rect.top.left)
        # Fix the rotation later
        window.blit(self.img, (self.x,self.y))

    def get_mask(self):
        return pygame.masl.from_surface(self.imgs)


def draw_window(window, Bird):
    window.blit(background_imgs, (0, 0))
    #window.blit(Bird.IMGS[0], (0, 0))
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
        #bird.move()
        draw_window(window, bird)


main()
