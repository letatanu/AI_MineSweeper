import numpy as np
import copy
from MineSweeper import *
class Agent:
    def __init__(self, Q_Matrix = None, lr = 0.1, gamma = 0.9, gameObject = None):

        self.gameObject = gameObject

        # Initializing Q_Matrix: dict{state: 8 actions Mtrix}
        # 0 1 2
        # 3 4 5
        # 6 7 8
        if Q_Matrix is None:
            self.Q_Matrix = {}
        else:
            self.Q_Matrix = Q_Matrix

        # learning rate
        self.lr = lr
        #gamma
        self.gamma = gamma

    # create a state from loc and grid, it will return a loc and its neighbor as
    # 0 1 2
    # 3 4 5
    # 6 7 8
    def createState(self, loc, grid):
        state = np.array([['-1']*3]*3)
        i,j = loc
        maxI = len(grid)
        maxJ = len(grid[0])
        state[1][1] = grid[i][j]
        if 0 <= i - 1:
            state[0][1] = grid[i-1][j]
            if 0 <= j-1:
                state[0][0] = grid[i-1][j-1]
            if maxJ > j+1:
                state[0][2] = grid[i-1][j+1]
        if 0 <= j-1:
            state[1][0] = grid[i][j-1]

        if maxJ > j + 1:
            state[1][2] = grid[i][j+1]
        if maxI > i+1:
            state[2][1] = grid[i+1][j]
            if 0 <= j-1:
                state[2][0] = grid[i+1][j-1]
            if maxJ > j+1:
                state[2][2] = grid[i+1][j+1]
        return state

    # convert an array to a string
    def arrayToString(self, array):
        return ".".join(str(x) for x in array)

    # get cells along border of uncovered and convered cells.
    def getBorderCells(self, grid):
        result = []
        maxI = len(grid)
        maxJ = len(grid[0])
        for i, row in enumerate(grid):
            for j, cell in enumerate(row):
                if 0 <= i - 1:
                    if grid[i - 1][j] == 'E':
                        result.append([i,j])
                        continue
                    if 0 <= j - 1:
                        if grid[i - 1][j - 1] == 'E':
                            result.append([i,j])
                            continue
                    if maxJ > j + 1:
                        if grid[i - 1][j + 1] == 'E':
                            result.append([i,j])
                            continue
                if 0 <= j - 1:
                    if grid[i][j - 1] == 'E':
                        result.append([i,j])
                        continue
                if maxJ > j + 1:
                    if grid[i][j + 1] == 'E':
                        result.append([i,j])
                        continue
                if maxI > i + 1:
                    if grid[i + 1][j] == 'E':
                        result.append([i,j])
                        continue
                    if 0 <= j - 1:
                        if grid[i + 1][j - 1] == 'E':
                            result.append([i,j])
                            continue
                    if maxJ > j + 1:
                        if grid[i + 1][j + 1] == 'E':
                            result.append([i,j])
                            continue
        return result


    def addNewState(self, state):
        # get current state
        newState = state.ravel().tolist()
        key = self.arrayToString(newState)
        if not key in self.Q_Matrix:
            self.Q_Matrix.update({key: np.zeros(9, dtype=np.float)})
            tmpState = np.zeros(9, dtype=np.float)
            for i, row in enumerate(newState):
                if row != 'E':
                    tmpState[i] = -np.inf
            key = self.arrayToString(newState)
            self.Q_Matrix.update({key: tmpState})
        return self.Q_Matrix[key]

    # get next state with a specific action
    # def nextState(self, action):
    #     return self.gameObject.playgame(action)

    def stateHavingMaxQ_Val(self, currentStates):
        comp = -99999
        state = ''
        location = [0,0]
        for currentState in currentStates:
            tmpState = self.createState(currentState, self.gameObject.currgrid)
            newState = tmpState.ravel().tolist()
            key = self.arrayToString(newState)
            a = np.max(self.Q_Matrix[key])
            if a > comp:
                comp = a
                state = key
                location = currentState
        return state, location

    def Q_s_b(self, action):
        a = self.gameObject.playgame(action)
        if a == -1:
            return [-1], -1
        currentStates = self.getBorderCells(self.gameObject.currgrid)
        for currentState in currentStates:
            newState = self.createState(currentState, self.gameObject.currgrid)
            self.addNewState(newState)

        # choosing an action from current states
        chosenState, location = self.stateHavingMaxQ_Val(currentStates)
        return self.Q_Matrix[chosenState], a

    def train(self, epsilon = 0.1):
        # epsilon
        self.epsilon = epsilon

        currentStates = self.getBorderCells(self.gameObject.currgrid)
        for currentState in currentStates:
            newState = self.createState(currentState,self.gameObject.currgrid)
            self.addNewState(newState)

        # choosing an action from current states
        chosenState, location = self.stateHavingMaxQ_Val(currentStates)
        action = np.argmax((self.Q_Matrix[chosenState] + np.random.randn(1, 9) * (1. / (self.epsilon + 1)))[0])

        newLocation = [location[0]+int(action/3)-1, location[1]+action%3-1]
        print(newLocation)
        Q_s_b, reward = self.Q_s_b(newLocation)
        self.Q_Matrix[chosenState][action] = self.Q_Matrix[chosenState][action] + self.lr * (reward + self.gamma * (np.max(Q_s_b)) - self.Q_Matrix[chosenState][action])
        if reward == -1:
            self.gameObject = MineSweeper(gridsize=self.gameObject.gridsize, numberOfMines=self.gameObject.numberofmines)
        return reward


