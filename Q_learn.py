import numpy as np



def env(params):


    global action, rewards, moveableArea, q_values

    action = ["UP", "DOWN", "LEFT", 'RIGHT']
    q_values = np.zeros((params['screenSizeX'], params['screenSizeY'], action))
    rewards = np.full([params['screenSizeX'], params['screenSizeY']], -100)
    rewards[params['food_posx'], params['food_posy']] = 100
    moveableArea = {}

    for i in range(1, params['screenSizeY']):
        moveableArea = [i for i in range(1, params['screenSizeX'])]  # come back to this

    for row_index in range(1, params['screenSizeX']):
        for column_index in moveableArea[row_index]:
            rewards[row_index, column_index] = -1
    return q_values


def is_terminal_state(current_row_index, current_column_index):
    if rewards[current_row_index, current_column_index] == -1:
        return False
    else:
        return True


def get_starting_location(params, e):
    current_row_index = params['snake_pos'][0]
    current_column_index = params['snake_pos'][1]
    while is_terminal_state(current_row_index, current_column_index):
        Move = np.random.choice([True, False], p=[1 - e, e])
    return Move


def get_next_action(params, current_row_index, current_column_index, e):
    moveBool = get_starting_location(params, e)
    if moveBool == False:
        return np.argmax(q_values[current_row_index, current_column_index])
    else:
        return True


def get_next_location(params, current_row_index, current_column_index, action_index):
    new_row_i = current_row_index
    new_col_i = current_column_index
    if action[action_index] == 'UP' and current_row_index > 0:
        new_row_i = 1
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
            current_row_index, current_column_index = get_next_location(current_row_index, current_column_index,
                                                                        action_index)
            shortest_path.append([current_row_index, current_column_index])
        return shortest_path


def Q_train(q_values, epsilon, gamma, learning_rate):
    for episode in range(1000):
        row_index, column_index = get_starting_location()
        q_values = [row_index, column_index, action]

    while not is_terminal_state(row_index, column_index):
        action_index = get_next_action(row_index, column_index, epsilon)

        old_row_index, old_column_index = row_index, column_index
        row_index, column_index = get_next_location(row_index, column_index, action_index)

        reward = rewards[row_index, column_index]
        old_q_value = q_values[old_row_index, old_column_index, action_index]
        temporal_difference = reward + (gamma * np.max(q_values[row_index, column_index])) - old_q_value

        new_q_value = old_q_value + (learning_rate * temporal_difference)
        q_values[old_row_index, old_column_index, action_index] = new_q_value

