# Making Frappy Bird with Pygame
# Scorce https://www.youtube.com/watch?v=3ZPQI2-ciWI

import pygame
import sys
import random


pygame.init()  # initialising the pygame, like main()

resolution_width = 576  #inital = 576
resolution_height = 1024  #inital = 1024

game_background = pygame.image.load("assets/picture/background-day.png").convert()
game_background = pygame.transform.scale(game_background, (resolution_width, resolution_height)) # STRECH the wallpaper


class TheBird:
    def __init__(self):
        self.x = 50
        self.y = 350
        self.jump = 0
        self.jump_speed = 10
        self.gravity = 10
        self.dead = False
        self.sprite = 0
        self.bird_sprites = [pygame.image.load("assets/picture/redbird-downflap.png").convert_alpha(),
                             pygame.image.load("assets/picture/redbird-midflap.png").convert_alpha(),
                             pygame.image.load("assets/picture/redbird-upflap.png").convert_alpha()]
    def move(self):
        if self.y > 0:
            if self.jump:
                self.sprite = 0
                self.jump_speed -= 1
                self.y -= self.jump_speed



class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((resolution_width, resolution_height))
        pygame.display.set_caption("Flappy Bird")
        self.background =  pygame.image.load("assets/picture/background-day.png").convert()  # background image
        self.bird = TheBird()  # bird object

    def run(self):
        done = True
        while done:
            for event in pygame.event.get():  # the block for quitting and prevent initial lopping 
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
            self.screen.blit(game_background, (0,0))
            self.screen.blit(self.background, (0, 0))
            self.screen.blit(self.bird.bird_sprites[self.bird.sprite], (self.bird.x, self.bird.y))



if __name__ == "__main__":
    game = Game()
    game.run()






'''   
    game_window.blit(self.TheBird.bird_sprites[self.TheBird.sprite], (self.TheBird.x, self.TheBird.y))
    game_window.blit(game_background, (0,0))
    pygame.display.update()
'''








'''
pong_ball = pygame.image.load("Pong_model\PongBall.png")
pong_ball = pygame.transform.scale(pong_ball, (ball_size, ball_size))
class Ball(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pong_ball
        self.rect = self.image.get_rect()
        self.rect.center = [x,y]

    def ballMove(self):
        self.rect.y += ball_y_vel
        self.rect.x += ball_x_vel
    
    def Reset(self, x, y):
        self.rect.center = [x,y]
'''


