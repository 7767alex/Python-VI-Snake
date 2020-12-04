import numpy as np

def env(params):

    global action, rewards, moveableArea, q_values
    rows = 2 + params['screenSizeX'] / 10
    columns = 2 + params['screenSizeY'] / 10
    action = ["UP", "DOWN", "LEFT", "RIGHT"]
    q_values = np.zeros((int(2 + params['screenSizeX']/10), int(2+params['screenSizeY'] / 10), 4))

    rewards = np.full([int(2+params['screenSizeX']/10), int(2+params['screenSizeY']/10)], -1)
    rewards[int(2+params['food_posx']/10), int(2+params['food_posy']/10)] = 500
    rewards[int(2+params['snake_pos'][0]/10), int(2+params['snake_pos'][1]/10)] = 50



    for i in range(int(columns)):
        rewards[0][int(i) - 1] = -100
        rewards[int(rows) - 1][int(i) - 1] = -100

    for i in range(int(rows)):
        rewards[int(i)][0] = -100
        rewards[int(i)][int(columns) - 1] = -100
    #print(rewards)

    return q_values

def is_terminal_state(current_row_index, current_column_index):
    #print(current_column_index)
    #print(current_row_index)
    if rewards[int(2+current_row_index), int(2+current_column_index)] == -1 or rewards[int(2+current_row_index), int(2+current_column_index)] == 5:
        print(rewards[int(2+current_row_index), int(2+current_column_index)])
       # print(current_column_index)
       # print(current_row_index)
        return False
    elif rewards[2 + int(current_row_index), 2 + int(current_column_index)] == -100:
        #print(current_column_index)
        #print(current_row_index)
        return True

def get_starting_location(params):
    current_row_index = params['snake_pos'][0] / 10
    current_column_index = params['snake_pos'][1] / 10
    #print(current_row_index + current_column_index)
    while is_terminal_state(current_row_index, current_column_index):
        current_row_index = params['snake_pos'][0] / 10
        current_column_index = params['snake_pos'][1] / 10
    return current_row_index, current_column_index

def get_next_action(params, current_row_index, current_column_index,epsilon):



    if np.random.random() < epsilon:
        return np.argmax(q_values[int(2+current_row_index/10), int(2+current_column_index/10)])
    else:
        return True



def get_next_location(params, current_row_index, current_column_index, action_index):
    new_row_i = current_row_index
    new_col_i = current_column_index

    if action[action_index] == 'UP' and current_row_index > 0:
        new_row_i -= 1
    elif action[action_index] == "RIGHT" and current_row_index < params['screenSizeX'] - 1:
        new_col_i += 1
    elif action[action_index] == "DOWN" and current_row_index < params['screenSizeY'] - 1:
        new_row_i += 1
    elif action[action_index] == "LEFT" and current_column_index > 0:
        new_col_i -= 1
    return new_row_i, new_col_i

def get_shortest_path(params, start_row_index, start_column_index):
    global action_index
    if is_terminal_state(start_row_index, start_column_index):
        return []
    else:
        current_row_index, current_column_index = start_row_index, start_column_index
        shortest_path = []
        shortest_path.append([current_row_index, current_column_index])

        while not is_terminal_state(current_row_index, current_column_index):
            action_index = get_next_action(params, current_row_index, current_column_index, 1)
            current_row_index, current_column_index = get_next_location(params, current_row_index, current_column_index,
                                                                        action_index)
            shortest_path.append([current_row_index, current_column_index])

        return action_index

def Q_train(params, epsilon, gamma, learning_rate):
    for episode in range(1):
        row_index, column_index = get_starting_location(params)
        row_index = 2 + row_index
        column_index = 2 + column_index
        #print(row_index)
        #print(column_index)

        while not is_terminal_state(row_index, column_index):
           # print(is_terminal_state(row_index, column_index))
            action_check = get_next_action(params, row_index, column_index, epsilon)

            #print(action_check)
            #print(column_index)
            if(action_check == True):
                action_index = np.random.randint(3)
            else:
                action_index = action_check


            old_row_index, old_column_index = row_index, column_index
            #print(get_next_location(params, row_index, column_index, action_index))
            row_index, column_index = get_next_location(params, row_index, column_index, action_index)
            #print(get_next_location(params, row_index, column_index, action_index))

            reward = rewards[int(row_index), int(column_index)]
            old_q_value = q_values[int(old_row_index), int(old_column_index), int(action_index)]
            temporal_difference = reward + (gamma * np.max(q_values[2])) - old_q_value

            new_q_value = old_q_value + (learning_rate * temporal_difference)
            q_values[int(old_row_index), int(old_column_index)] = new_q_value
            #print(q_values)
            #print(q_values)

print("training complete")
            #print(q_values)
