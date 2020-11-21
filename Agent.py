import numpy as np
import sys
from collections import defaultdict
import pickle
from time import sleep, time

if sys.argv[1] == "p":
    mode = "play"
if sys.argv[1] == "t": ##button
    mode = "train"

if mode == "play":
    import snake
else:
    import snake_headless

rewardAlive = -1
rewardKill = -10000
rewardScore = 50000000

alpha = 0.1
alphaD = 0.999
# alphe --> learnRate
# alphaD --> Zerfallsrate

gamma = 0.9
# discount factor

if mode == "play":
    e = 0.0001
    ed = 1
    emin = 0.0001
else:
    e = 0.9
    ed = 1.3
    emin = 0.0001
# ed zerfallsrate von e
# epsilon --> randomness


try:
    with open("Q_val.pickle", "rb") as Qval:
        Q = defaultdict(lambda: [0, 0, 0, 0], pickle.load(Qval)) ##load Q values
except:
    Q = defaultdict(lambda: [0, 0, 0, 0])
    # U,L,D,R
    print("NEW Q")

lastMoves = ""

oldState = None
oldAction = None
gameCounter = 0
gameScores = []

def states(params):

    global lastMoves
    rFP = ""  # als String concatenated
    sB = ""  # als String concatenated
    bP = ""  # as String concatenated
    skip = 0
    direction = ""




    relativeFoodPostion = np.zeros(6)
    Screen_border = np.zeros(4)
    body_prox = np.zeros(4)
    snake_body = np.array()



    if (params["food_pos"][0] - params["snake_pos"][0]) > 0:  # foodRight
        relativeFoodPostion[0] = 1
    if (params["food_pos"][0] - params["snake_pos"][0]) < 0:  # foodLeft
        relativeFoodPostion[1] = 1
    if ((params["food_pos"][0] - params["snake_pos"][0]) == 0):  # foodXMiddle
        relativeFoodPostion[2] = 1

    if (params["food_pos"][1] - params["snake_pos"][1]) > 0:  # foodDown
        relativeFoodPostion[3] = 1
    if (params["food_pos"][1] - params["snake_pos"][1]) < 0:  # foodTop
        relativeFoodPostion[4] = 1
    if ((params["food_pos"][1] - params["snake_pos"][1]) == 0):  # foodYMiddle
        relativeFoodPostion[5] = 1


    for x in relativeFoodPostion:
        rFP += str(x)



    if (params["screenSizeX"] - params["snake_pos"][0] == 10):  # dangerRight
        Screen_border[0] = 1
    if (params["screenSizeX"] - params["snake_pos"][0] == params["screenSizeX"]):  # dangerLeft
        Screen_border[1] = 1
    if (params["screenSizeY"] - params["snake_pos"][1] == 10):  # dangerBottom
        Screen_border[2] = 1
    if (params["screenSizeY"] - params["snake_pos"][1] == params["screenSizeY"]):  # dangerTop
        Screen_border[3] = 1


    for x in Screen_border:
        sB += str(x)





    for pos in params["snake_body"]:
        if (skip > 3):
            snake_body.append(pos)
        skip += 1


    for bodyPart in snake_body:
        # print(bodyPart)
        if (params["snake_pos"][0] - bodyPart[0] == 0 and params["snake_pos"][1] - bodyPart[1] == 10):  # BodyPartUp
            body_prox[0] = 1
        if (params["snake_pos"][0] - bodyPart[0] == 0 and params["snake_pos"][1] - bodyPart[1] == -10):  # BodypartDown
            body_prox[1] = 1
        if (params["snake_pos"][0] - bodyPart[0] == 10 and params["snake_pos"][1] - bodyPart[1] == 0):  # BodyPartLeft
            body_prox[2] = 1
        if (params["snake_pos"][0] - bodyPart[0] == -10 and params["snake_pos"][1] - bodyPart[1] == 0):  # BodypartRight
            body_prox[3] = 1


    for x in body_prox:
        bP += str(x)

    dx = params["snake_body"][1][0] - params["snake_body"][0][0]
    dy = params["snake_body"][1][1] - params["snake_body"][0][1]

    if dx == -10 and dy == 0:
        # Moving right
        direction = "0"
    if dx == 10 and dy == 0:
        # Moving left
        direction = "1"
    if dx == 0 and dy == 10:
        # Moving up
        direction = "2"
    if dx == 0 and dy == -10:
        # Moving down
        direction = "3"


    state = rFP + "_" + sB + "_" + bP + "_" + direction
    return state





def actions(params):
    global curr_state
    global curr_action

    state = states(params)
    estReward = Q[state]

    curr_reward = Q[curr_state]

    index = 0
    if curr_action == 'U':
        index = 0
    if curr_action == 'L':
        index = 1
    if curr_action == 'D':
        index = 2
    if curr_action == 'R':
        index = 3

    # reward more negative, when taking many moves to score; reset, when food is eaten
    reward = (0 - params["moveSinceScore"]) / 50

    curr_reward[index] = (1 - alpha) * curr_reward[index] + \
                        alpha * (reward + gamma * max(estReward))

    Q[curr_state] = curr_reward

    curr_state = state
    basedOnQ = np.random.choice([True, False], p=[1 - e, e])

    if basedOnQ == False:
        choice = np.random.choice(['U', 'L', 'D', 'R'], p=[0.25, 0.25, 0.25, 0.25])
        curr_state = choice
        return choice
    else:
        if estReward[0] > estReward[1] and estReward[0] > estReward[2] and estReward[0] > estReward[3]:
            curr_state = 'U'
            return 'U'
        if estReward[1] > estReward[0] and estReward[1] > estReward[2] and estReward[1] > estReward[3]:
            curr_state = 'L'
            return 'L'
        if estReward[2] > estReward[0] and estReward[2] > estReward[1] and estReward[2] > estReward[3]:
            curr_state = 'D'
            return 'D'
        if estReward[3] > estReward[0] and estReward[3] > estReward[1] and estReward[3] > estReward[2]:
            curr_state = 'R'
            return 'R'
        else:
            choice = np.random.choice(['U', 'L', 'D', 'R'], p=[0.25, 0.25, 0.25, 0.25])
            curr_state = choice
            return choice


gameCounter = []
gameCounter = 0
start = 0
end = 0


def onGameOver(score, moves):
    global oldState
    global oldAction
    global gameCounter
    global alpha, e, ed
    global start, end

    gameScores.append(score)

    # update Q of previous state (state which lead to gameOver)
    prevReward = Q[oldState]

    if oldAction == None:
        index = 0
    if oldAction == 'U':
        index = 0
    if oldAction == 'L':
        index = 1
    if oldAction == 'D':
        index = 2
    if oldAction == 'R':
        index = 3

    prevReward[index] = (1 - alpha) * prevReward[index] + \
                        alpha * rewardKill

    Q[oldState] = prevReward

    oldState = None
    oldAction = None

    # save Q as pickle
    if gameCounter % 200 == 0:
        with open("Q_value" + ".pickle", "wb") as QVal:
            pickle.dump(dict(Q), Qval)
        print("+++++++++ Pickle saved +++++++++")

    # show some stats
    if gameCounter % 100 == 1:
        end = time()
        timeD = end - start
        print(str(gameCounter) + " : " + "\t" + 'meanScore: ' + str(np.mean(gameScores[-100:])) + "| HighScore: " + str(
            np.max(gameScores)) + \
              '| moves: ' + str(np.mean(moves[-100:])) + "| time for 10 games: " + str(round(timeD * 10) / 100))
        start = time()

    # print coeffients
    if gameCounter % 100 == 0:
        print("a:", alpha)
        print("e:", e)
        print("g:", gamma)

    # decrease alpha / e over time(moves)
    if gameCounter % 100 == 0:
        alpha = alpha * alphaD
        if e > emin:
            e = e / ed

    gameCounter += 1


def onScore(params):
    global oldState
    global oldAction
    global gameCounter

    state = states(params)

    estReward = Q[state]

    prevReward = Q[oldState]

    if oldAction == 'U':
        index = 0
    if oldAction == 'L':
        index = 1
    if oldAction == 'D':
        index = 2
    if oldAction == 'R':
        index = 3

    prevReward[index] = (1 - alpha) * prevReward[index] + \
                        alpha * (rewardScore + gamma * max(estReward))

    Q[oldState] = prevReward


if mode == "play":
    snake.main(actions, onGameOver, onScore)
else:
    snake_headless.main(actions, onGameOver, onScore)
