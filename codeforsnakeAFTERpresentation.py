# This is a sample Python script.

# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.
''' Notes For Instructor: This is the updated project. All variables are the same as the collab FOR READABILITY AMONG THE GROUP. If you are curious about the collab email me about it on canvas since
I get my notifications from there. This is work done after the presentation on Tuesday. I managed to get the moves to work and I wanted to see the QLearning train in
action. The concept is there and I have thoroughly studied it. Ask any questions that you may have to my canvas email.Algorithm had to be rewritten twice. The first algorithm 
moved around but only left to right.'''

import pygame
import random
import time
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

def our_snake(snake_block,snake_list_np) :     #Extend the snake

    row = snake_list_np.shape
    a = (row[0]/2)

    for b in range(int(a)):
        #print("B values", snake_list_np[b*2], " ", snake_list_np[b*2+1])
        pygame.draw.rect(dis,black,[snake_list_np[b*2],snake_list_np[b*2+1],snake_block,snake_block])
    #for a in snake_list:
    #    print("A value in our_snake",a)
    #    pygame.draw.rect(dis,black,[a[0],a[1],snake_block,snake_block])
def check_food(obstacle_array):
    obstacles = obstacle_array.shape
    num_obstacles = (obstacles[0] / 2)

    foodx = round(random.randrange(0, dis_width - snake_block) / 10.0) * 10.0
    foody = round(random.randrange(0, dis_height - snake_block) / 10.0) * 10.0

    # print("FOOD X ", foodx)
    # print("FOOD Y ", foody)

    while (True):
        temp = []
        for a in range(int(num_obstacles)):
            if (int(obstacle_array[a * 2]) == foodx and int(obstacle_array[a * 2 + 1]) == foody):
                foodx = round(random.randrange(0, dis_width - snake_block) / 10.0) * 10.0
                foody = round(random.randrange(0, dis_height - snake_block) / 10.0) * 10.0
                temp = [foodx, foody]
        temp.append(foodx)
        temp.append(foody)
        # print("TEMP", temp)
        # print("FOOD X ", foodx)
        # print("FOOD Y ", foody)
        return temp

def game_loop_QResult():
    game_over = False
    game_close = False
     # will contains the head indexes
    x1 = dis_width / 2  # initial value for x
    y1 = dis_height / 2 # initial value for y


    x1_change = 0
    y1_change = 0

    foodx = round(random.randrange(0, dis_width - snake_block) / 10.0) * 10.0
    foody = round(random.randrange(0, dis_height - snake_block) / 10.0) * 10.0

    snake_list = []
    snake_length = 1
    snake_list_np = np.array([])




    prev_direction = "LEFT"
    next_move = "LEFT"

    while (not game_over):
        while game_close == True:
            dis.fill(white)
            message("Press Q to quit or C to Play")
            pygame.display.update()

            ############    AGENT ACTION SHOULD BE DETERMINED BY HERE   ############
            ############    OR BEFORE THE GAME_CLOSE LOOP IS ENTERED   ############
        for event in pygame.event.get():  # In the case of game over start or quit
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:  # Case of quit game_over = true
                    game_over = True
                    game_close = False
                if event.key == pygame.K_c:  # Case of start again, loop again
                    game_loop_QResult()

        if event.type == pygame.KEYDOWN:  # if key is pressed

            if event.key == pygame.K_LEFT:  # Case of lef key
                x1_change = -snake_block
                y1_change = 0
            if event.key == pygame.K_RIGHT:  # Case of right key
                x1_change = snake_block
                y1_change = 0
            if event.key == pygame.K_UP:  # Case of up key
                # print("HIT")
                y1_change = -snake_block
                x1_change = 0
            if event.key == pygame.K_DOWN:  # Case of down key
                # print("HIT")
                y1_change = snake_block
                x1_change = 0

        newevent = pygame.event.Event(pygame.KEYDOWN, unicode="left arrow", key=pygame.K_LEFT,
                                      mod=pygame.KMOD_NONE)  # create the event
        pygame.event.post(newevent)

        if (next_move == "left"):
            newevent = pygame.event.Event(pygame.KEYDOWN, unicode="left arrow", key=pygame.K_LEFT,
                                          mod=pygame.KMOD_NONE)  # create the event
            pygame.event.post(newevent)
        elif (next_move == "right"):
            newevent = pygame.event.Event(pygame.KEYDOWN, unicode="right arrow", key=pygame.K_RIGHT,
                                          mod=pygame.KMOD_NONE)  # create the event
            pygame.event.post(newevent)
        elif (next_move == "up"):
            newevent = pygame.event.Event(pygame.KEYDOWN, unicode="up arrow", key=pygame.K_UP,
                                          mod=pygame.KMOD_NONE)  # create the event
            pygame.event.post(newevent)
        elif (next_move == "down"):
            newevent = pygame.event.Event(pygame.KEYDOWN, unicode="down arrow", key=pygame.K_DOWN,
                                          mod=pygame.KMOD_NONE)  # create the event
            pygame.event.post(newevent)

        for event in pygame.event.get():  # For input during game
            # print(event)  # For every input print it out
            if event.type == pygame.QUIT:  # In the case that anything input attempts to close window
                game_over = True  # Set game_over to true

            ############    AGENT ACTION SHOULD BE DETERMINED BY HERE   ############
            ############    OR BEFORE THE GAME_CLOSE LOOP IS ENTERED   ############

            if event.type == pygame.KEYDOWN:  # if key is pressed

                if event.key == pygame.K_LEFT:  # Case of lef key
                    x1_change = -snake_block
                    y1_change = 0
                if event.key == pygame.K_RIGHT:  # Case of right key
                    x1_change = snake_block
                    y1_change = 0
                if event.key == pygame.K_UP:  # Case of up key
                    # print("HIT")
                    y1_change = -snake_block
                    x1_change = 0
                if event.key == pygame.K_DOWN:  # Case of down key
                    # print("HIT")
                    y1_change = snake_block
                    x1_change = 0
        ##############################################
        ######## MOVE HAS BEEN TAKEN INTO ACCOUNT FOR THE SNAKE ########################
        if x1 >= dis_width or x1 < 0 or y1 >= dis_height or y1 < 0:  # the case that the snake hits a border
            game_close = True

        x1 = x1 + x1_change  # Updated y and x positions of snake
        y1 = y1 + y1_change

        dis.fill(white)  # Fil display with white

        snake_Head = [x1, y1]

        snake_list_np = np.append(snake_list_np, snake_Head)
        row = snake_list_np.shape
        snake_len = (row[0] / 2)

        if int(snake_len) > snake_length:
            # del snake_list[0]
            snake_list_np = np.delete(snake_list_np, [0, 1])

        row = snake_list_np.shape
        snake_len = (row[0] / 2)

        for a in range(int(snake_len - 1)):
            # print("For loop np ", snake_list_np[a*2], " ", snake_list_np[a*2+1])
            if (int(snake_list_np[a * 2]) == x1 and int(snake_list_np[a * 2 + 1]) == y1):
                game_close = True

        our_snake(snake_block, snake_list_np)

        pygame.draw.rect(dis, blue, [foodx, foody, snake_block, snake_block])  # Draw food pellet
        pygame.draw.rect(dis, black,
                         [x1, y1, snake_block, snake_block])  # position of rectangle 200,150 and then size 10,10

        pygame.display.update()  # Update what is in window

        if x1 == foodx and y1 == foody:  # Case of head running into food
            # check_food(obstacle_array,foodx,foody)
            foodx = round(random.randrange(0, dis_width - snake_block) / 10.0) * 10.0
            foody = round(random.randrange(0, dis_height - snake_block) / 10.0) * 10.0
            snake_length = snake_length + 1  # Extend snake and replace old food pellet
            # print("Yummy")

        params = {
            'food_posx': foodx,
            'food_posy': foody,
            'snake_pos': snake_Head,
            'snake_body': snake_list_np,
            'score': snake_length,
            'screenSizeX': dis_width,
            'screenSizeY': dis_height,

        }

        Q.env(params)
        row_index, column_index = Q.get_starting_location(params)
        row_index = row_index
        column_index = column_index
        learning_rate = 0.2
        gamma = 0.8
        epsilon = 0.3
        # new = 1
        # print(row_index)
        # print(column_index)
        # print(row_index, column_index)
        victory = 0
        if not Q.is_terminal_state(params, row_index, column_index):
            action_index = Qlearn(params, epsilon, gamma, learning_rate,row_index, column_index,victory)
            print("Next MOVE: ", next_move)
            if action_index == 0:
                next_move = "up"
            if action_index == 1:
                next_move = "down"
            if action_index == 2:
                next_move = "left"
            if action_index == 3:
                next_move = "right"

        prev_direction = next_move
        #newevent = pygame.event.Event(pygame.KEYDOWN, unicode = "left arrow", key =pygame.k_a, mod=pygame.KMOD_NONE)
        pygame.event.post(newevent)
        #clock.tick(snake_speed)

    pygame.quit()
    quit()


def Q_learnAlg(params, row_index, column_index):
    if ((2 + params['snake_pos'][0] / 10) == (2 + params['screenSizeX'] / 10) or (2 + params['snake_pos'][1] / 10) == (2 + params['screenSizeY'] / 10)):
        reward = -100
        return reward
    else:
        reward = Q.rewards[int(row_index - 1), int(column_index-1)]
        return reward
def Qlearn(params, epsilon, gamma, learning_rate,row_index, column_index,victory):
    # print("in while loop")
    # print(is_terminal_state(row_index, column_index))
    action_index = Q.get_next_action(params, row_index, column_index, epsilon)

    print(" ")
    print("snakePos: " + " X: " + str(2 + params['snake_pos'][0] / 10) + " y" + str(2 + params['snake_pos'][1] / 10))
    print("FoodPos: " + " X: " + str(2 + params['food_posx'] / 10) + " Y: " + str(2 + params['food_posy'] / 10))
    print("BorderPos: " + " X: " + str(2 + params['screenSizeX'] / 10) + " Y: " + str(2 + params['screenSizeY'] / 10))
    print(" ")
    print("nextMove:")

    # print(column_index)

    old_row_index, old_column_index = row_index, column_index
    # print(get_next_location(params, row_index, column_index, action_index))
    row_index, column_index = Q.get_next_location(params, row_index, column_index, action_index)
    # print(get_next_location(params, row_index, column_index, action_index))
    reward = Q_learnAlg(params, row_index, column_index)
    old_q_value = Q.q_values[int(old_row_index), int(old_column_index), int(action_index)]
    temporal_difference = reward + (gamma * np.max(Q.q_values[2])) - old_q_value

    new_q_value = old_q_value + (learning_rate * temporal_difference)
    Q.q_values[int(old_row_index), int(old_column_index)] = new_q_value

    if (int(2 + params['snake_pos'][0] / 10) == int(2 + params['food_posx'] / 10) and int(
            2 + params['snake_pos'][1] / 10) == int(2 + params['food_posy'] / 10)):
        victory += 1

        # print("victory!!!")
    if (int(2 + params['snake_pos'][0] / 10) == int(2 + params['screenSizeX'] / 10) and int(
            2 + params['food_posy'] / 10) == int(2 + params['screenSizeY'] / 10)):
        victory -= 1
        print("dang")
    return action_index


    print(" ")
    print("training complete")
    print(" ")
    print("summary of training:")
    print("TimesFoodEatenFullRound: " + str(victory))
    print(" ")
    print("shortest Path: ")
    print(" ")

game_loop_QResult()





