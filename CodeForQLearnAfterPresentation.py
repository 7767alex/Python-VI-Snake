''' Notes For Instructor: This is the updated project. All variables are the same as the collab. If you are curious about the collab email me about it on canvas since
I get my notifications from there. This is work done after the presentation on Tuesday. I managed to get the moves to work and I wanted to see the QLearning train in
action. The concept is there and I have thoroughly studied it. Ask any questions that you may have to my canvas email.Algorithm had to be rewritten twice. The first algorithm 
moved around but only left to right.'''


import numpy as np

def env(params):

    global action, rewards, moveableArea, q_values
    rows = 2 + params['screenSizeX'] / 10
    columns = 2 + params['screenSizeY'] / 10
    action = ["UP", "DOWN", "LEFT", "RIGHT"]
    q_values = np.zeros((int(2 + params['screenSizeX']/10), int(2+params['screenSizeY'] / 10), 4))

    rewards = np.full([int(2+params['screenSizeX']/10), int(2+params['screenSizeY']/10)], 1)
    rewards[int(2+params['food_posx']/10), int(2+params['food_posy']/10)] = 50
    rewards[int(2+params['snake_pos'][0]/10), int(2+params['snake_pos'][1]/10)] = 10
    #for i in range (1,(2+ params['snake_body']/10)):
        #rewards[int(2+params['snake_body'][i]/10)] = -10
    
    #print(rewards)



    for i in range(int(columns)):
        rewards[0][int(i) - 1] = -100
        rewards[int(rows) - 1][int(i) - 1] = -100

    for i in range(int(rows)):
        rewards[int(i)][0] = -100
        rewards[int(i)][int(columns) - 1] = -100
    #print(rewards)

    return q_values,rows,columns,action,rewards

def is_terminal_state(params, current_row_index, current_column_index):
    #print(current_column_index)
    #print(current_row_index)
    if rewards[int(2+current_row_index/10), int(2+current_column_index/10)] == -1 or rewards[int(2+current_row_index/10), int(2+current_column_index/10)] == 5:
       # print(rewards)
       #print(rewards[int(2+current_row_index/10), int(2+current_column_index/10)])
       # print(current_column_index)
       # print(current_row_index)
        return False
    elif (2 + params['snake_pos'][0] / 10) >= (2 + params['screenSizeX'] / 10) or (2 + params['snake_pos'][1] / 10) >= (2 + params['screenSizeY'] / 10):
        #print(current_column_index)
        #print(current_row_index)
        return True

def get_starting_location(params):
    params['snake_pos'][0] = 50
    params['snake_pos'][1] = 50
    current_row_index = 2+ params['snake_pos'][0] / 10

    current_column_index = 2+ params['snake_pos'][1] / 10
    #print(current_row_index + current_column_index)
    while is_terminal_state(params, current_row_index, current_column_index):
        current_row_index = 2+ params['snake_pos'][0] / 10
        current_column_index = 2+ params['snake_pos'][1] / 10
    return current_row_index, current_column_index

def get_next_action(params, current_row_index, current_column_index,epsilon):



    if np.random.random() < epsilon:
        #print("max" + str(np.argmax(q_values[int(2 + current_row_index / 10), int(2 + current_column_index / 10)])))
        return np.argmax(q_values[int(2+current_row_index/10), int(2+current_column_index/10)])

    else:
        #print("rand" + str(np.random.randint(4)))
        return np.random.randint(4)




def get_next_location(params, current_row_index, current_column_index, action_index):
    new_row_i = current_row_index
    new_col_i = current_column_index

    if action[action_index] == 'UP' and current_row_index > 0:
        params['snake_pos'][1] += 10
        new_row_i = 2 + params['snake_pos'][1] / 10
    elif action[action_index] == "RIGHT" and current_row_index < params['screenSizeX'] - 1:
        params['snake_pos'][0] += 10
        new_col_i = 2 + params['snake_pos'][0]/10
    elif action[action_index] == "DOWN" and current_row_index < params['screenSizeY'] - 1:
        params['snake_pos'][1] -= 10
        new_row_i = 2 + params['snake_pos'][1]/10
    elif action[action_index] == "LEFT" and current_column_index > 0:
        params['snake_pos'][0] -= 10
        new_col_i = 2 + params['snake_pos'][0]/10
    #print("snakePos:" + "X:" + str(2 + params['snake_pos'][0]/10) + "y" + str(2 + params['snake_pos'][1]/10))
    #print("FoodPos: " + "X: " + str(2+params['food_posx']/10) + "Y: " + str(2+params['food_posy']/10))
    #print("BorderPos: " + "X: " + str(2+params['screenSizeX']/10) + "Y: " + str(2+params['screenSizeY']/10))
    return new_row_i, new_col_i



