
import pygame
import time
import random
import numpy as np
import snake as sn



def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press ⌘F8 to toggle the breakpoint.


# Press the green button in the gutter to run the script.
pygame.init()  # Initialize everything at the start

dis_width = 600 # Width and height of the screen
dis_height = 400

dis = pygame.display.set_mode((dis_width, dis_height))  # Set setting for the display
pygame.display.set_caption('Snake Game RL')  # Caption for window

blue = (0, 0, 255)  # RGB value for blue
red = (255, 0, 0)  # RGB value for red
white = (255, 255, 255)  # RGB value for white
green = (0,255,0) #RGB value for green
black = (0, 0, 0)  # RGB value for black

x1 = 300  # inital value for x
y1 = 300  # initial value for y

x1_change = 0
y1_change = 0
snake_block = 10    #Size of the snake
snake_speed = 15    #Amount of frames per second

font_style = pygame.font.SysFont(None, 50)

backgroundmenu = pygame.image.load('menu.png')
backgroundmenu = pygame.transform.scale(backgroundmenu, (dis_width, dis_height))
pausemenu = pygame.image.load('gamepause.png')
pausemenu = pygame.transform.scale(pausemenu, (dis_width, dis_height))


def main_menu():
    menu = True
    while menu:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:  # User clicks x to close window
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:  # User presses Q
                if event.key == pygame.K_q:
                    pygame.quit()
                    quit()
                if event.key == pygame.K_t:  # User presses 1
                    sn.game_loop_Train()
                    menu = False
                if event.key == pygame.K_p:  # User presses 2
                    sn.game_loop_Q()
                    menu = False

        dis.blit(backgroundmenu, (0, 0))
        pygame.display.update()

main_menu()
