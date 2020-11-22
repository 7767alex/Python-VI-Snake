# This is a sample Python script.

# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.
import pygame
import time
import random
import numpy as np


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


def our_snake(snake_block,snake_list_np) :     #Extend the snake

    row = snake_list_np.shape
    a = (row[0]/2)

    for b in range(int(a)):
        #print("B values", snake_list_np[b*2], " ", snake_list_np[b*2+1])
        pygame.draw.rect(dis,black,[snake_list_np[b*2],snake_list_np[b*2+1],snake_block,snake_block])
    #for a in snake_list:
    #    print("A value in our_snake",a)
    #    pygame.draw.rect(dis,black,[a[0],a[1],snake_block,snake_block])


def message(msg):  # Function for the display output of game over
    mesg = font_style.render(msg, True, red)
    dis.blit(mesg, [0, 100])


pygame.display.update()  # Update used to update any parameters passed onto the screen
game_over = False  # Bool value that indicates if game should end
game_close = False
clock = pygame.time.Clock()


def game_loop1():

    game_over = False
    game_close = False

    x1 = dis_width/2  # inital value for x
    y1 = dis_height/2  # initial value for y

    x1_change = 0 #x and y values to be added to x and y
    y1_change = 0

    #print("HIT1")

    foodx = round(random.randrange(0, dis_width - snake_block) / 10.0) * 10.0
    foody = round(random.randrange(0, dis_height - snake_block) / 10.0) * 10.0

    snake_list = [] #Contains the extended snake including head
    snake_length = 1 #Inital length of snake

    snake_list_np = np.array([])

    while (not game_over): #The game and display updates happen here

        while game_close == True:
            dis.fill(white)
            message("Press Q to quit or C to Play")
            pygame.display.update()

            for event in pygame.event.get(): #In the case of game over start or quit
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q: #Case of quit game_over = true
                        game_over = True
                        game_close = False
                    if event.key == pygame.K_c: #Case of start again, loop again
                        game_loop()

        for event in pygame.event.get():  # For input during game
            #print(event)  # For every input print it out
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

        if x1 >= dis_width or x1 < 0 or y1 >= dis_height or y1 < 0:  # the case that the snake hits a border
            game_close = True

        x1 = x1 + x1_change  # Updated y and x positions of snake
        y1 = y1 + y1_change

        dis.fill(white)  # Fil display with white

        snake_Head = [] #will contains the head indexes
        snake_Head.append(x1)
        snake_Head.append(y1)

        snake_list_np = np.append(snake_list_np,snake_Head)
        row = snake_list_np.shape
        snake_len = (row[0] / 2)

        #if len(snake_list) > snake_length: #Deleting the snake that is no longer there
        if int(snake_len) > snake_length:
            #del snake_list[0]
            snake_list_np = np.delete(snake_list_np, [0,1])

        row = snake_list_np.shape
        snake_len = (row[0] / 2)

        for a in range(int(snake_len-1)):
            #print("For loop np ", snake_list_np[a*2], " ", snake_list_np[a*2+1])
            if(int(snake_list_np[a*2]) == x1 and int(snake_list_np[a*2+1]) == y1):
                game_close = True

        #for a in snake_list[:-1]: #Case that snake runs into itself
        #    print("For loop [:-1] ",a)
        #    #print("a in snake_list: ",a);
        #    if a == snake_Head:
        #        game_close = True


        #our_snake(snake_block,snake_list,snake_list_np)
        our_snake(snake_block,snake_list_np)

        pygame.draw.rect(dis, blue, [foodx, foody, snake_block, snake_block]) #Draw food pellet
        pygame.draw.rect(dis, black, [x1, y1, snake_block, snake_block])  # position of rectangle 200,150 and then size 10,10

        #### Following code is for the obstacles, not adjusted for custom display height and width

        obstacle1x = 90
        obstacle1y = 100
        obstacle_array = np.array([])
        obstacle_array = np.append(obstacle_array,[obstacle1x,obstacle1y])
        pygame.draw.rect(dis,red,[obstacle1x,obstacle1y, snake_block,snake_block])

        obstacle1x = 100
        obstacle1y = 100
        obstacle_array = np.append(obstacle_array, [obstacle1x, obstacle1y])
        pygame.draw.rect(dis,red,[obstacle1x,obstacle1y, snake_block,snake_block])

        obstacle1x = 110
        obstacle1y = 100
        obstacle_array = np.append(obstacle_array, [obstacle1x, obstacle1y])
        pygame.draw.rect(dis,red,[obstacle1x,obstacle1y, snake_block,snake_block])

        obstacle1x = 120
        obstacle1y = 100
        obstacle_array = np.append(obstacle_array, [obstacle1x, obstacle1y])
        pygame.draw.rect(dis,red,[obstacle1x,obstacle1y, snake_block,snake_block])

        obstacle1x = 130
        obstacle1y = 100
        obstacle_array = np.append(obstacle_array, [obstacle1x, obstacle1y])
        pygame.draw.rect(dis,red,[obstacle1x,obstacle1y, snake_block,snake_block])

        obstacle1x = 140
        obstacle1y = 100
        obstacle_array = np.append(obstacle_array, [obstacle1x, obstacle1y])
        pygame.draw.rect(dis,red,[obstacle1x,obstacle1y, snake_block,snake_block])

        obstacle1x = 150
        obstacle1y = 100
        obstacle_array = np.append(obstacle_array, [obstacle1x, obstacle1y])
        pygame.draw.rect(dis,red,[obstacle1x,obstacle1y, snake_block,snake_block])

        obstacle1x = 160
        obstacle1y = 100
        obstacle_array = np.append(obstacle_array, [obstacle1x, obstacle1y])
        pygame.draw.rect(dis,red,[obstacle1x,obstacle1y, snake_block,snake_block])

        obstacle1x = 170
        obstacle1y = 100
        obstacle_array = np.append(obstacle_array, [obstacle1x, obstacle1y])
        pygame.draw.rect(dis,red,[obstacle1x,obstacle1y, snake_block,snake_block])

        obstacle1x = 180
        obstacle1y = 100
        obstacle_array = np.append(obstacle_array, [obstacle1x, obstacle1y])
        pygame.draw.rect(dis,red,[obstacle1x,obstacle1y, snake_block,snake_block])

        obstacle1x = 190
        obstacle1y = 100
        obstacle_array = np.append(obstacle_array, [obstacle1x, obstacle1y])
        pygame.draw.rect(dis,red,[obstacle1x,obstacle1y, snake_block,snake_block])

        obstacle1x = 200
        obstacle1y = 100
        obstacle_array = np.append(obstacle_array, [obstacle1x, obstacle1y])
        pygame.draw.rect(dis,red,[obstacle1x,obstacle1y, snake_block,snake_block])

        obstacle1x = 210
        obstacle1y = 100
        obstacle_array = np.append(obstacle_array, [obstacle1x, obstacle1y])
        pygame.draw.rect(dis,red,[obstacle1x,obstacle1y, snake_block,snake_block])

        obstacle1x = 220
        obstacle1y = 100
        obstacle_array = np.append(obstacle_array, [obstacle1x, obstacle1y])
        pygame.draw.rect(dis,red,[obstacle1x,obstacle1y, snake_block,snake_block])

        obstacle1x = 230
        obstacle1y = 100
        obstacle_array = np.append(obstacle_array, [obstacle1x, obstacle1y])
        pygame.draw.rect(dis,red,[obstacle1x,obstacle1y, snake_block,snake_block])

        obstacle1x = 240
        obstacle1y = 100
        obstacle_array = np.append(obstacle_array, [obstacle1x, obstacle1y])
        pygame.draw.rect(dis,red,[obstacle1x,obstacle1y, snake_block,snake_block])

        obstacle1x = 250
        obstacle1y = 100
        obstacle_array = np.append(obstacle_array, [obstacle1x, obstacle1y])
        pygame.draw.rect(dis,red,[obstacle1x,obstacle1y, snake_block,snake_block])

        obstacle1x = 260
        obstacle1y = 100
        obstacle_array = np.append(obstacle_array, [obstacle1x, obstacle1y])
        pygame.draw.rect(dis,red,[obstacle1x,obstacle1y, snake_block,snake_block])

        obstacle1x = 270
        obstacle1y = 100
        obstacle_array = np.append(obstacle_array, [obstacle1x, obstacle1y])
        pygame.draw.rect(dis,red,[obstacle1x,obstacle1y, snake_block,snake_block])

        obstacle1x = 280
        obstacle1y = 100
        obstacle_array = np.append(obstacle_array, [obstacle1x, obstacle1y])
        pygame.draw.rect(dis,red,[obstacle1x,obstacle1y, snake_block,snake_block])

        obstacle1x = 290
        obstacle1y = 100
        obstacle_array = np.append(obstacle_array, [obstacle1x, obstacle1y])
        pygame.draw.rect(dis,red,[obstacle1x,obstacle1y, snake_block,snake_block])

        obstacle1x = 300
        obstacle1y = 100
        obstacle_array = np.append(obstacle_array, [obstacle1x, obstacle1y])
        pygame.draw.rect(dis,red,[obstacle1x,obstacle1y, snake_block,snake_block])

        obstacle1x = 310
        obstacle1y = 100
        obstacle_array = np.append(obstacle_array, [obstacle1x, obstacle1y])
        pygame.draw.rect(dis,red,[obstacle1x,obstacle1y, snake_block,snake_block])

        obstacle1x = 320
        obstacle1y = 100
        obstacle_array = np.append(obstacle_array, [obstacle1x, obstacle1y])
        pygame.draw.rect(dis,red,[obstacle1x,obstacle1y, snake_block,snake_block])

        obstacle1x = 330
        obstacle1y = 100
        obstacle_array = np.append(obstacle_array, [obstacle1x, obstacle1y])
        pygame.draw.rect(dis,red,[obstacle1x,obstacle1y, snake_block,snake_block])

        obstacle1x = 340
        obstacle1y = 100
        obstacle_array = np.append(obstacle_array, [obstacle1x, obstacle1y])
        pygame.draw.rect(dis,red,[obstacle1x,obstacle1y, snake_block,snake_block])

        obstacle1x = 350
        obstacle1y = 100
        obstacle_array = np.append(obstacle_array, [obstacle1x, obstacle1y])
        pygame.draw.rect(dis,red,[obstacle1x,obstacle1y, snake_block,snake_block])

        obstacle1x = 360
        obstacle1y = 100
        obstacle_array = np.append(obstacle_array, [obstacle1x, obstacle1y])
        pygame.draw.rect(dis,red,[obstacle1x,obstacle1y, snake_block,snake_block])

        obstacle1x = 370
        obstacle1y = 100
        obstacle_array = np.append(obstacle_array, [obstacle1x, obstacle1y])
        pygame.draw.rect(dis,red,[obstacle1x,obstacle1y, snake_block,snake_block])

        obstacle1x = 380
        obstacle1y = 100
        obstacle_array = np.append(obstacle_array, [obstacle1x, obstacle1y])
        pygame.draw.rect(dis,red,[obstacle1x,obstacle1y, snake_block,snake_block])

        obstacle1x = 390
        obstacle1y = 100
        obstacle_array = np.append(obstacle_array, [obstacle1x, obstacle1y])
        pygame.draw.rect(dis,red,[obstacle1x,obstacle1y, snake_block,snake_block])

        obstacle1x = 400
        obstacle1y = 100
        obstacle_array = np.append(obstacle_array, [obstacle1x, obstacle1y])
        pygame.draw.rect(dis,red,[obstacle1x,obstacle1y, snake_block,snake_block])

        obstacle1x = 410
        obstacle1y = 100
        obstacle_array = np.append(obstacle_array, [obstacle1x, obstacle1y])
        pygame.draw.rect(dis,red,[obstacle1x,obstacle1y, snake_block,snake_block])

        obstacle1x = 80
        obstacle1y = 100
        obstacle_array = np.append(obstacle_array, [obstacle1x, obstacle1y])
        pygame.draw.rect(dis,red,[obstacle1x,obstacle1y, snake_block,snake_block])

        obstacle1x = 70
        obstacle1y = 100
        obstacle_array = np.append(obstacle_array, [obstacle1x, obstacle1y])
        pygame.draw.rect(dis,red,[obstacle1x,obstacle1y, snake_block,snake_block])

        obstacle1x = 60
        obstacle1y = 100
        obstacle_array = np.append(obstacle_array, [obstacle1x, obstacle1y])
        pygame.draw.rect(dis,red,[obstacle1x,obstacle1y, snake_block,snake_block])

        obstacle1x = 50
        obstacle1y = 100
        obstacle_array = np.append(obstacle_array, [obstacle1x, obstacle1y])
        pygame.draw.rect(dis,red,[obstacle1x,obstacle1y, snake_block,snake_block])

        obstacle1x = 40
        obstacle1y = 100
        obstacle_array = np.append(obstacle_array, [obstacle1x, obstacle1y])
        pygame.draw.rect(dis,red,[obstacle1x,obstacle1y, snake_block,snake_block])

        obstacle1x = 30
        obstacle1y = 100
        obstacle_array = np.append(obstacle_array, [obstacle1x, obstacle1y])
        pygame.draw.rect(dis,red,[obstacle1x,obstacle1y, snake_block,snake_block])

        obstacles = obstacle_array.shape
        num_obstacles = (obstacles[0] / 2)


        for a in range(int(num_obstacles)):
            if(int(obstacle_array[a*2]) == x1 and int(obstacle_array[a*2+1]) == y1):
                game_close = True


        pygame.display.update()  # Update what is in window

        if x1 == foodx and y1 == foody: #Case of head running into food
            foodx = round(random.randrange(0, dis_width - snake_block) / 10.0) * 10.0
            foody = round(random.randrange(0, dis_height - snake_block) / 10.0) * 10.0
            snake_length = snake_length+1 #Extend snake and replace old food pellet
            #print("Yummy")

        #Gerardo_Conversion(obstacle_array,foodx,foody,snake_list_np)



        clock.tick(snake_speed)  # 30 frames for every second

    pygame.quit()
    quit()  # Uninitialize everything at the end


def game_loop2():

    game_over = False
    game_close = False

    x1 = dis_width/2  # inital value for x
    y1 = dis_height/2  # initial value for y

    x1_change = 0 #x and y values to be added to x and y
    y1_change = 0

    #print("HIT1")

    foodx = round(random.randrange(0, dis_width - snake_block) / 10.0) * 10.0
    foody = round(random.randrange(0, dis_height - snake_block) / 10.0) * 10.0

    snake_list = [] #Contains the extended snake including head
    snake_length = 1 #Inital length of snake

    snake_list_np = np.array([])

    while (not game_over): #The game and display updates happen here

        while game_close == True:
            dis.fill(white)
            message("Press Q to quit or C to Play")
            pygame.display.update()

            for event in pygame.event.get(): #In the case of game over start or quit
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q: #Case of quit game_over = true
                        game_over = True
                        game_close = False
                    if event.key == pygame.K_c: #Case of start again, loop again
                        game_loop()

        for event in pygame.event.get():  # For input during game
            #print(event)  # For every input print it out
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

        if x1 >= dis_width or x1 < 0 or y1 >= dis_height or y1 < 0:  # the case that the snake hits a border
            game_close = True

        x1 = x1 + x1_change  # Updated y and x positions of snake
        y1 = y1 + y1_change

        dis.fill(white)  # Fil display with white

        snake_Head = [] #will contains the head indexes
        snake_Head.append(x1)
        snake_Head.append(y1)

        snake_list_np = np.append(snake_list_np,snake_Head)
        row = snake_list_np.shape
        snake_len = (row[0] / 2)

        #if len(snake_list) > snake_length: #Deleting the snake that is no longer there
        if int(snake_len) > snake_length:
            #del snake_list[0]
            snake_list_np = np.delete(snake_list_np, [0,1])

        row = snake_list_np.shape
        snake_len = (row[0] / 2)

        for a in range(int(snake_len-1)):
            #print("For loop np ", snake_list_np[a*2], " ", snake_list_np[a*2+1])
            if(int(snake_list_np[a*2]) == x1 and int(snake_list_np[a*2+1]) == y1):
                game_close = True

        #for a in snake_list[:-1]: #Case that snake runs into itself
        #    print("For loop [:-1] ",a)
        #    #print("a in snake_list: ",a);
        #    if a == snake_Head:
        #        game_close = True


        #our_snake(snake_block,snake_list,snake_list_np)
        our_snake(snake_block,snake_list_np)

        pygame.draw.rect(dis, blue, [foodx, foody, snake_block, snake_block]) #Draw food pellet
        pygame.draw.rect(dis, black, [x1, y1, snake_block, snake_block])  # position of rectangle 200,150 and then size 10,10

        #### Following code is for the obstacles, not adjusted for custom display height and width

        obstacle1x = 90
        obstacle1y = 100
        obstacle_array = np.array([])
        obstacle_array = np.append(obstacle_array,[obstacle1x,obstacle1y])
        pygame.draw.rect(dis,red,[obstacle1x,obstacle1y, snake_block,snake_block])

        obstacle1x = 300
        obstacle1y = 70
        obstacle_array = np.append(obstacle_array, [obstacle1x, obstacle1y])
        pygame.draw.rect(dis,red,[obstacle1x,obstacle1y, snake_block,snake_block])

        obstacle1x = 390
        obstacle1y = 110
        obstacle_array = np.append(obstacle_array, [obstacle1x, obstacle1y])
        pygame.draw.rect(dis,red,[obstacle1x,obstacle1y, snake_block,snake_block])

        obstacle1x = 40
        obstacle1y = 400
        obstacle_array = np.append(obstacle_array, [obstacle1x, obstacle1y])
        pygame.draw.rect(dis,red,[obstacle1x,obstacle1y, snake_block,snake_block])

        obstacle1x = 230
        obstacle1y = 100
        obstacle_array = np.append(obstacle_array, [obstacle1x, obstacle1y])
        pygame.draw.rect(dis,red,[obstacle1x,obstacle1y, snake_block,snake_block])

        obstacle1x = 140
        obstacle1y = 100
        obstacle_array = np.append(obstacle_array, [obstacle1x, obstacle1y])
        pygame.draw.rect(dis,red,[obstacle1x,obstacle1y, snake_block,snake_block])

        obstacle1x = 350
        obstacle1y = 200
        obstacle_array = np.append(obstacle_array, [obstacle1x, obstacle1y])
        pygame.draw.rect(dis,red,[obstacle1x,obstacle1y, snake_block,snake_block])

        obstacle1x = 260
        obstacle1y = 200
        obstacle_array = np.append(obstacle_array, [obstacle1x, obstacle1y])
        pygame.draw.rect(dis,red,[obstacle1x,obstacle1y, snake_block,snake_block])

        obstacle1x = 370
        obstacle1y = 100
        obstacle_array = np.append(obstacle_array, [obstacle1x, obstacle1y])
        pygame.draw.rect(dis,red,[obstacle1x,obstacle1y, snake_block,snake_block])

        obstacle1x = 180
        obstacle1y = 100
        obstacle_array = np.append(obstacle_array, [obstacle1x, obstacle1y])
        pygame.draw.rect(dis,red,[obstacle1x,obstacle1y, snake_block,snake_block])

        obstacle1x = 190
        obstacle1y = 100
        obstacle_array = np.append(obstacle_array, [obstacle1x, obstacle1y])
        pygame.draw.rect(dis,red,[obstacle1x,obstacle1y, snake_block,snake_block])

        obstacle1x = 200
        obstacle1y = 100
        obstacle_array = np.append(obstacle_array, [obstacle1x, obstacle1y])
        pygame.draw.rect(dis,red,[obstacle1x,obstacle1y, snake_block,snake_block])

        obstacle1x = 210
        obstacle1y = 100
        obstacle_array = np.append(obstacle_array, [obstacle1x, obstacle1y])
        pygame.draw.rect(dis,red,[obstacle1x,obstacle1y, snake_block,snake_block])

        obstacle1x = 220
        obstacle1y = 100
        obstacle_array = np.append(obstacle_array, [obstacle1x, obstacle1y])
        pygame.draw.rect(dis,red,[obstacle1x,obstacle1y, snake_block,snake_block])

        obstacle1x = 290
        obstacle1y = 400
        obstacle_array = np.append(obstacle_array, [obstacle1x, obstacle1y])
        pygame.draw.rect(dis,red,[obstacle1x,obstacle1y, snake_block,snake_block])

        obstacle1x = 240
        obstacle1y = 300
        obstacle_array = np.append(obstacle_array, [obstacle1x, obstacle1y])
        pygame.draw.rect(dis,red,[obstacle1x,obstacle1y, snake_block,snake_block])

        obstacle1x = 350
        obstacle1y = 300
        obstacle_array = np.append(obstacle_array, [obstacle1x, obstacle1y])
        pygame.draw.rect(dis,red,[obstacle1x,obstacle1y, snake_block,snake_block])

        obstacle1x = 230
        obstacle1y = 10
        obstacle_array = np.append(obstacle_array, [obstacle1x, obstacle1y])
        pygame.draw.rect(dis,red,[obstacle1x,obstacle1y, snake_block,snake_block])


        obstacles = obstacle_array.shape
        num_obstacles = (obstacles[0] / 2)


        for a in range(int(num_obstacles)):
            if(int(obstacle_array[a*2]) == x1 and int(obstacle_array[a*2+1]) == y1):
                game_close = True


        pygame.display.update()  # Update what is in window

        if x1 == foodx and y1 == foody: #Case of head running into food
            foodx = round(random.randrange(0, dis_width - snake_block) / 10.0) * 10.0
            foody = round(random.randrange(0, dis_height - snake_block) / 10.0) * 10.0
            snake_length = snake_length+1 #Extend snake and replace old food pellet
            #print("Yummy")

        #Gerardo_Conversion(obstacle_array,foodx,foody,snake_list_np)



        clock.tick(snake_speed)  # 30 frames for every second

    pygame.quit()
    quit()  # Uninitialize everything at the end

def game_loop():

    game_over = False
    game_close = False

    x1 = dis_width/2  # inital value for x
    y1 = dis_height/2  # initial value for y

    x1_change = 0 #x and y values to be added to x and y
    y1_change = 0

    #print("HIT1")

    foodx = round(random.randrange(0, dis_width - snake_block) / 10.0) * 10.0
    foody = round(random.randrange(0, dis_height - snake_block) / 10.0) * 10.0

    snake_list = [] #Contains the extended snake including head
    snake_length = 1 #Inital length of snake

    snake_list_np = np.array([])

    while (not game_over): #The game and display updates happen here

        while game_close == True:
            dis.fill(white)
            message("Press Q to quit or C to Play")
            pygame.display.update()

            for event in pygame.event.get(): #In the case of game over start or quit
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q: #Case of quit game_over = true
                        game_over = True
                        game_close = False
                    if event.key == pygame.K_c: #Case of start again, loop again
                        game_loop()

        for event in pygame.event.get():  # For input during game
            #print(event)  # For every input print it out
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

        if x1 >= dis_width or x1 < 0 or y1 >= dis_height or y1 < 0:  # the case that the snake hits a border
            game_close = True

        x1 = x1 + x1_change  # Updated y and x positions of snake
        y1 = y1 + y1_change

        dis.fill(white)  # Fil display with white

        snake_Head = [] #will contains the head indexes
        snake_Head.append(x1)
        snake_Head.append(y1)

        snake_list_np = np.append(snake_list_np,snake_Head)
        row = snake_list_np.shape
        snake_len = (row[0] / 2)

        #if len(snake_list) > snake_length: #Deleting the snake that is no longer there
        if int(snake_len) > snake_length:
            #del snake_list[0]
            snake_list_np = np.delete(snake_list_np, [0,1])

        row = snake_list_np.shape
        snake_len = (row[0] / 2)

        for a in range(int(snake_len-1)):
            #print("For loop np ", snake_list_np[a*2], " ", snake_list_np[a*2+1])
            if(int(snake_list_np[a*2]) == x1 and int(snake_list_np[a*2+1]) == y1):
                game_close = True

        #for a in snake_list[:-1]: #Case that snake runs into itself
        #    print("For loop [:-1] ",a)
        #    #print("a in snake_list: ",a);
        #    if a == snake_Head:
        #        game_close = True


        #our_snake(snake_block,snake_list,snake_list_np)
        our_snake(snake_block,snake_list_np)

        pygame.draw.rect(dis, blue, [foodx, foody, snake_block, snake_block]) #Draw food pellet
        pygame.draw.rect(dis, black, [x1, y1, snake_block, snake_block])  # position of rectangle 200,150 and then size 10,10

        pygame.display.update()  # Update what is in window

        if x1 == foodx and y1 == foody: #Case of head running into food
            foodx = round(random.randrange(0, dis_width - snake_block) / 10.0) * 10.0
            foody = round(random.randrange(0, dis_height - snake_block) / 10.0) * 10.0
            snake_length = snake_length+1 #Extend snake and replace old food pellet
            #print("Yummy")

        clock.tick(snake_speed)  # 30 frames for every second

    pygame.quit()
    quit()  # Uninitialize everything at the end


game_loop2()
#print("HIT3")

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
