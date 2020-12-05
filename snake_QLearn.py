# This is a sample Python script.
#author Travis Quigg
#current issues:
#body isn't in the grid
# isn't emulating moves in game
# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.
import pygame
import random
import numpy as np
import Q_learn as Q

pygame.init()  # Initialize everything at the start

# Original values for both is 600 by 400
dis_width = 100 # Width and height of the screen
dis_height = 100

dis = pygame.display.set_mode((dis_width, dis_height))  # Set setting for the display
pygame.display.set_caption('Snake Game RL')  # Caption for window

blue = (0, 0, 255)  # RGB value for blue
red = (255, 0, 0)  # RGB value for red
white = (255, 255, 255)  # RGB value for white
green = (0,255,0) #RGB value for green
black = (0, 0, 0)  # RGB value for black

x1 = 50  # inital value for x
y1 = 50  # initial value for y

x1_change = 0
y1_change = 0
snake_block = 10    #Size of the snake
snake_speed = 10    #Amount of frames per second (original is 15)

font_style = pygame.font.SysFont(None, 50)


def game_loop_Train():
    game_over = False
    game_close = False
     # will contains the head indexes
    x1 = dis_width / 2  # initial value for x
    y1 = dis_height / 2 # initial value for y
    snake_Head = [x1, y1]
    moveCounter = 0
    moves = []
    moveSinceScore = 0
    snake_list_np = np.array([])
    snake_list_np = np.append(snake_list_np, snake_Head)
    snake_length = 1

    # print("HIT1")
    ##[120, 100]
    foodx = round(random.randrange(0, dis_width - snake_block) / 10.0) * 10.0
    foody = round(random.randrange(0, dis_height - snake_block) / 10.0) * 10.0



    params = {
        'food_posx': foodx,
        'food_posy': foody,
        'snake_pos': snake_Head,
        'snake_body': snake_list_np,
        'score': snake_length,
        # 'diff':diff,
        'screenSizeX': dis_width,
        'screenSizeY': dis_height,
        'moveSinceScore': moveSinceScore
    }

    environment = Q.env(params)

    change_to = ''
    learning_rate = 0.2
    gamma = 0.8
    epsilon = 0.3

    Q.Q_train(params, epsilon, gamma, learning_rate)
    #game_loop_Q(environment)


game_loop_Train()
