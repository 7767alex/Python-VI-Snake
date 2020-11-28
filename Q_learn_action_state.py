import numpy as np
from collections import defaultdict
import pickle
from time import sleep, time

currState = None
currAction = None
gameCounter = 0
gameScores = []

try:
    with open("Q_val" + ".pickle", "rb") as Q_val:
        Q = defaultdict(lambda: [0,0,0,0], pickle.load(Q_val))
except:
    Q = defaultdict(lambda: [0,0,0,0])
    #UP LEFT DOWN RIGHT
    print("NEW Q")

lastMoves = ""

def states(params):
    global oldMoves
    relaFoodPosition = "NOTHING"
    screenBorder = np.zeros(6)
    bodyProx = np.zeros(4)
    snakeBody = np.array()

    RelaState = ""
    ScreenState = ""
    BodyState = ""


    if ((params["food_pos"][0] - params["snake_pos"][0]) > 0):
        relaFoodPosition[0] = "RI"
    if((params["food_pos"][0] - params["snake_pos"][0])< 0):
        relaFoodPosition[1] = "LE"
    if ((params["food_pos"][0] - params["snake_pos"][0]) == 0):
        relaFoodPosition[2] = "MX"
    if (params["food_pos"][1] - params["snake_pos"][1]) > 0:
        relaFoodPosition[3] = "DO"
    if (params["food_pos"][1] - params["snake_pos"][1]) < 0:
        relaFoodPosition[4] = "UP"
    if ((params["food_pos"][1] - params["snake_pos"][1]) == 0):
        relaFoodPosition[5] = "MY"

    for i in relaFoodPosition:
        RelaState += str(i)

    if (params["screenSizeX"] - params["snake_pos"][0] == 10):
        screenBorder[0] = "RI"
    if (params["screenSizeX"] - params["snake_pos"][0] == params["screenSizeX"]):
        screenBorder[1] ="LE"
    if (params["screenSizeY"] - params["snake_pos"][1] == -10):
        screenBorder[2] = "DO"
    if (params["screenSizeY"] - params["snake_pos"][1] == params["screenSizeY"]):
        screenBorder[3] = "UP"

    for i in screenBorder:
        ScreenState += str(i)

    next = 0
    for i in params["snake_body"]:
        if(next > 3):
            snakeBody.append(i)
        next+=1

    for bodyProx_ in snakeBody:
        if (params["snake_pos"][0] - bodyProx_[0] == 0 and params["snake_pos"][1] - bodyProx_[1] == 10):
            bodyProx[0] = "UP"
        if (params["snake_pos"][0] - bodyProx_[0] == 0 and params["snake_pos"][1] - bodyProx_[1] == -10):
            bodyProx[1] = "DO"
        if (params["snake_pos"][0] - bodyProx_[0] == 10 and params["snake_pos"][1] - bodyProx_[1] == 0):
            bodyProx[2] = "LE"
        if (params["snake_pos"][0] - bodyProx_[0] == -10 and params["snake_pos"][1] - bodyProx_[1] == 0):
            bodyProx[3] = "RI"

    for i in bodyProx:
        BodyState += str(i)

    direction = ""
    direct = [params["snake_body"][1][0] - params["snake_body"][0][0],
              params["snake_body"][1][1] - params["snake_body"][0][1]]
                ##(x,y)

    if (direct[0] == 10 and direct[1] == 0):
        direction = "RI"
    if (direct[0] == -10 and direct[1] == 0):
        direction = "LE"
    if(direct[0] == 0 and direct[1] == 10):
        direction = "UP"
    if (direct[0] == 0 and direct[1] == -10):
        direction = "DO"

    state = np.array()
    state.append(RelaState)
    state.append(ScreenState)
    state.append(BodyState)

gameCounter = []
gameCounter = 0
start = 0
end = 0

def QLearning(params, Q, alpha, gamma, e):

  global currState, currAction, gameCounter, start, end

  choice = np.random.choice(['U', 'D', 'R', 'L'], p=[0.25, 0.25, 0.25, 0.25])
  FirstMove = np.random.choice([True, False], p=[1-e,e])

  state = QLearning(params, Q, alpha, gamma, e)
  futReward = Q[state]
  currReward = Q[currState]

  i = 0

  if (currAction == 'U'):
      i = 0
  if (currAction == 'D'):
      i = 1
  if(currAction == 'R'):
      i = 2
  if(currAction == 'L'):
      i = 3
  ###Aproximate Q-Learning####

  reward = ((0 - params["moveSinceScore"]) /50)
  sample = alpha * (reward + gamma * max(futReward))
  currReward[i] = (1-alpha) * currReward[i] + sample

  Q[currState] = currReward

  if FirstMove == False:
      currAction = choice
      return currAction
  else:
      if futReward[0] > (futReward[1] and futReward[2] and futReward[3] and futReward[4]):
          currAction = 'U'
          return currAction
      if futReward[1] > (futReward[0] and futReward[2] and futReward[3] and futReward[4]):
          currAction = 'D'
          return currAction
      if futReward[2] > (futReward[0] and futReward[1] and futReward[3] and futReward[4]):
          currAction = 'R'
          return currAction
      if futReward[3] > (futReward[0] and futReward[1] and futReward[2] and futReward[4]):
          currAction = 'L'
          return currAction

      else:
          currAction = choice
          return currAction

  if (gameCounter % 200 == 0):
      with open("Q_val" + ".pickle", "wb") as Q_val:
          pickle.dump(dict(Q), Q_val)

  if (gameCounter % 100 == 1):
      end = time()
      timeD = end-start
      start = time()

  if gameCounter % 100 == 0:
      alpha = alpha * alphaD
      if e > emin:
          e = e / ed

  gameCounter += 1
