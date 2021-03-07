import pygame
import os
import random
import pandas as pd
import csv
import re
from os import path
pygame.font.init()

WIN_WIDTH = 500
WIN_HEIGHT = 800
WHITE = (255,255,255)
D_between_pipes = 700
win = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
global run
run = True
click = pygame.MOUSEBUTTONDOWN
FRAMERATE = int(60)
VELOCITY_OBJECT = 2 #inital is 4 for 30fps
D_between_pipes = 700  # distance of pipe spawning



BIRD_IMGS = [pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "bird1.png"))), pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "bird2.png"))), pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "bird3.png")))]
PIPE_IMG = pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "pipe.png")))
BASE_IMG = pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "base.png")))
BG_IMGS = pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "bg.png")))
STAT_FONT = pygame.font.SysFont("comicsans", 50)



###############################################

class Bird:
    #inital_img = 
    IMGS = BIRD_IMGS
    MAX_ROTATION = 25
    ROT_VEL = 20
    ANIMATION_TIME = 5
    
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.tilt = 0
        self.tick_count = 0
        self.vel = 0 
        self.height = self.y
        self.img_count = 0
        self.img = BIRD_IMGS[0]
        self.IMGS = BIRD_IMGS
        self.bird_rect = self.img.get_rect()

    def jump(self):
        self.vel = -7 * VELOCITY_OBJECT
        self.tick_count = 0
        self.height = self.y
    
    def move(self):
        self.tick_count += 1

        d = ((self.vel*(self.tick_count) + 1.5*self.tick_count**2)/5)*VELOCITY_OBJECT

        if d >= 3.2*VELOCITY_OBJECT:
            d = 4*VELOCITY_OBJECT
        if d < 0:
            d -= 0.4*VELOCITY_OBJECT
        
        self.y = self.y + d

        if d < 0 or self.y < self.height + 50:
            if self.tilt < self.MAX_ROTATION:
                self.tilt = self.MAX_ROTATION
        else:
            if self.tilt > -90:
                self.tilt -= self.ROT_VEL

    def draw(self, win):
        self.img_count += 1

        if self.img_count < self.ANIMATION_TIME:
            self.img = self.IMGS[0]
        elif self.img_count < self.ANIMATION_TIME*2:
            self.img = self.IMGS[1]
        elif self.img_count < self.ANIMATION_TIME*3:
            self.img = self.IMGS[2]
        elif self.img_count < self.ANIMATION_TIME*4:
            self.img = self.IMGS[1]
        elif self.img_count < self.ANIMATION_TIME*4 +1:
            self.img = self.IMGS[0]
            self.img_count = 0
        
        if self.tilt <= -80:
            self.img = self.IMGS[1]
            self.img_count = self.ANIMATION_TIME*2
        
        rotated_image = pygame.transform.rotate(self.img, self.tilt)
        new_rect = rotated_image.get_rect(center=self.img.get_rect(topleft =(self.x, self.y)).center)
        win.blit(rotated_image, new_rect.topleft)
    
    def get_mask(self):
        return pygame.mask.from_surface(self.img)


class Pipe:
    GAP = 200
    VEL = VELOCITY_OBJECT

    def __init__(self, x):
        self.x = x
        self.height = 0 
        self.gap = 100

        self.top = 0 
        self.bottom = 0
        self.PIPE_TOP = pygame.transform.flip(PIPE_IMG, False, True)
        self.PIPE_BOTTOM = PIPE_IMG

        self.passed = False
        self.set_height()
        self.pipe_img_rect_top = self.PIPE_TOP.get_rect
        self.pipe_img_rect_bottom = self.PIPE_BOTTOM.get_rect
    
    def set_height(self):
        self.height = random.randrange(50, 450)
        self.top = self.height - self.PIPE_TOP.get_height()
        self.bottom = self.height + self.GAP
    
    def move(self):
        self.x -= self.VEL
    
    def draw(self, win):
        win.blit(self.PIPE_TOP, (self.x, self.top))
        win.blit(self.PIPE_BOTTOM, (self.x, self.bottom))

    def collide(self, bird, win):
        """
        returns if a point is colliding with the pipe
        :param bird: Bird object
        :return: Bool
        """
        bird_mask = bird.get_mask()
        top_mask = pygame.mask.from_surface(self.PIPE_TOP)
        bottom_mask = pygame.mask.from_surface(self.PIPE_BOTTOM)
        top_offset = (self.x - bird.x, self.top - round(bird.y))
        bottom_offset = (self.x - bird.x, self.bottom - round(bird.y))

        b_point = bird_mask.overlap(bottom_mask, bottom_offset)
        t_point = bird_mask.overlap(top_mask,top_offset)

        if b_point or t_point:
            return True

        return False


class Base:
    VEL = VELOCITY_OBJECT
    WIDTH = BASE_IMG.get_width()
    IMG = BASE_IMG

    def __init__(self, y):
        self.y = y
        self.x1 = 0
        self.x2 = self.WIDTH
    
    def move(self):
        self.x1 -= self.VEL
        self.x2 -= self.VEL

        if self.x1 + self.WIDTH < 0:
            self.x1 = self.x2 + self.WIDTH
        if self.x2 + self.WIDTH < 0:
            self.x2 = self.x1 + self.WIDTH

    def draw(self, win):
        win.blit(self.IMG, (self.x1, self.y))
        win.blit(self.IMG, (self.x2, self.y))


click = pygame.MOUSEBUTTONDOWN
class Button():
    def __init__(self, x, y, text = ''):
        self.color = (0)
        self.width = WIN_WIDTH*0.4
        self.height = WIN_WIDTH*0.09
        self.x = x
        self.y = y
        self.text = text
    def draw(self, centertext): 
        #outline
        pygame.draw.rect(win, WHITE, (self.x - self.width/2 - 4, self.y - self.height/2 - 4, self.width + 8, self.height + 8), 0)

        #button
        pygame.draw.rect(win, self.color, (self.x - self.width/2, self.y - self.height/2, self.width, self.height), 0)
        
        if self.text != '':
            font = pygame.font.SysFont('Corbel', 40)
            word = font.render(self.text, 0 , WHITE)
            win.blit(word, (self.x - centertext, self.y - self.height/2 + 5))

    #mouse interaction with button
    def isOver(self, mouse_position):
        if ((mouse_position[0] >= (self.x - self.width/2)) and (mouse_position[0] <= (self.x + self.width/2))) and ((mouse_position[1] >= (self.y - self.height/2)) and (mouse_position[1] <= (self.y + self.height/2))):
            self.color = (100 , 100, 100)           
            return True
        else: 
            self.color = (0)


class LeaderBoard:
    def __init__(self, x, y, text = ''):
        self.color = (0)
        self.width = WIN_WIDTH*0.4
        self.height = WIN_WIDTH*0.09
        self.x = x
        self.y = y
        self.text = text
    
    def draw(y): # spacing y = 40
        #try:
        with open('FrappyBird_Score.csv', 'r', newline='') as score_file:
            player_reader = csv.reader(score_file, delimiter=',')
            row_count = sum(1 for row in player_reader)

        with open('FrappyBird_Score.csv') as player_file:
            player_reader = csv.reader(player_file, delimiter=',')
            for row_key in list(player_reader)[1:row_count]:
                text = STAT_FONT.render(str(row_key), 1, (255, 255, 255))
                win.blit(text, (WIN_WIDTH/2 - text.get_width()/2, y))
                y += 40


    def save_score(score):
        try:
            new_name = "GameN"
            new_high_score = score
            with open('FrappyBird_Score.csv', 'a', newline='') as score_file:
                    player_writer = csv.writer(score_file, delimiter=',')
                    player_writer.writerow([new_name, new_high_score])
        except:
            #No csv found, a csv will be created with header
            print("log: No csv not found, a csv named FrappyBird_Score")
            with open('FrappyBird_Score.csv', 'w', newline='') as score_file:
                player_writer = csv.writer(score_file, delimiter=',')
                player_writer.writerow(['Name', 'High Score'])
            write_to_csv(new_name, new_high_score)


###############################################

def menu_draw(win, bird, base, mouse_pos, event):
    global start_button
    global option_button
    global exit_button
    start_button = Button(bird.x + 25, bird.y + 400, 'Start')
    option_button = Button(bird.x, bird.y + 225, 'Options')
    exit_button = Button(bird.x, bird.y + 300, 'Exit')
    win.blit(BG_IMGS, (0, 0))
    base.draw(win)
    bird.draw(win)
    text = STAT_FONT.render("Welcome to Frappy Bird", 1, (255, 255, 255))
    win.blit(text, (WIN_WIDTH/2 - text.get_width()/2, 10))
    LeaderBoard.draw(10+40) # y
    start_button.draw(70)
    #option_button.draw(105)
    #exit_button.draw(55)
    pygame.display.update()
    return start_button, exit_button, option_button

def menu_mode():
        menu_draw(win, bird, base, mouse_pos, event)
        if event.type == pygame.KEYDOWN and bird_is_alive == True:
            gameplay_mode(win, bird, pipes, base, score, event, clock, bird_is_alive)  


def gamplay_draw(win, bird, pipes, base, score, event):
    win.blit(BG_IMGS, (0, 0))
    for pipe in pipes:
        pipe.draw(win)
    
    text = STAT_FONT.render("Score: " + str(score), 1, (255, 255, 255))
    win.blit(text, (WIN_WIDTH - 10 - text.get_width(), 10))
    
    base.draw(win)
    bird.draw(win)
    pygame.display.update()

def gameplay_mode(win, bird, pipes, base, score, event, clock, bird_is_alive):
    while bird_is_alive == True:
        clock.tick(FRAMERATE)  # Framerate tied to the Timing
        bird.move()
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                bird.jump()
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
        
        add_pipe = False
        rem = []
        for pipe in pipes:
            pipe.move()
            # check for collision
            if pipe.collide(bird, win):
                LeaderBoard.save_score(score)
                bird_is_alive = False
                main()
            if pipe.x + pipe.PIPE_TOP.get_width() < 0:
                rem.append(pipe)
            if not pipe.passed and pipe.x < bird.x:
                pipe.passed = True
                add_pipe = True
            pipe.move()

        if add_pipe:
            score += 1 
            pipes.append(Pipe(D_between_pipes))
        for r in rem:
            pipes.remove(r)  # delete the pipe
        if bird.y + bird.img.get_height() >= 730:
            pass
        base.move()
        gamplay_draw(win, bird, pipes, base, score, event)


def main():
    global win, mouse_pos, bird, pipes, base, score, event, clock, bird_is_alive, run
    score = 0
    bird = Bird(230, 350)
    base = Base(730)
    pipes = [Pipe(D_between_pipes)]
    clock = pygame.time.Clock()
    run = True
    mouse_pos = pygame.mouse.get_pos()
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                bird_is_alive = False
                run = False
            if event.type == pygame.KEYDOWN:
                bird.jump()
        menu_mode()
        
        
    pygame.quit()
    quit()

bird_is_alive = True
main()

'''
import pandas as pd
from io import StringIO
import re

for_pd = StringIO()
with open('MikeS159.csv') as mike:
    for line in mike:
        new_line = re.sub(r',', '|', line.rstrip(), count=7)
        print (new_line, file=for_pd)

for_pd.seek(0)

df = pd.read_csv(for_pd, sep='|', header=None)
print (df)




add this 
https://stackoverflow.com/questions/27713855/how-to-get-an-input-from-user-in-pygame-and-save-it-as-a-variable
def ask(screen, question):
    "ask(screen, question) -> answer"
    pygame.font.init()
    current_string = []
    display_box(screen, question + ": " + string.join(current_string,""))
    while 1:
      inkey = get_key()
      if inkey == K_BACKSPACE:
        current_string = current_string[0:-1]
      elif inkey == K_RETURN:
        break
      elif inkey == K_MINUS:
        current_string.append("_")
      elif inkey <= 127:
        current_string.append(chr(inkey))
      display_box(screen, question + ": " + string.join(current_string,""))
    return string.join(current_string,"")
'''

