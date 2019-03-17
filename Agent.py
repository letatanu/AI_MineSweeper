import numpy as np

class Agent:
    def __init__(self, Q_Matrix = None, lr = 0.1, gamma = 0.9, epsilon = 0.1):


        # Initializing Q_Matrix: dict{state: 8 actions Mtrix}
        # 0 1 2
        # 3 _ 4
        # 5 6 7

        if Q_Matrix is None:
            self.Q_Matrix = {}
        else:
            self.Q_Matrix = Q_Matrix

        # learning rate
        self.lr = lr
        #gamma
        self.gamma = gamma
        #epsilon
        self.epsilon = epsilon

    # convert an array to a string
    def arrayToString(self, array):
        return ".".join(str(x) for x in array)


    def addNewState(self, state):
        # get current state
        newState = state.ravel().tolist()
        key = self.arrayToString(newState)
        if not key in self.Q_Matrix:
            self.Q_Matrix.update({key: np.zeros(self.size * self.size, dtype=np.float)})
            tmpState = np.zeros(self.size * self.size, dtype=np.float)
            for i, row in enumerate(newState):
                if row != -1:
                    tmpState[i] = -np.inf
            key = self.arrayToString(newState)
            self.Q_Matrix.update({key: tmpState})
        return self.Q_Matrix[key]
    # get next state with a specific action
    def nextState(self, grid, action):


