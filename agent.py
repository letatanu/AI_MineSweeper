import numpy as np
import random
import os
import itertools
import copy
import tensorflow as tf

class agent(object):
    '''the agent implementing q-learning algorithm'''

    def __init__(self):
        self.eta = 0.9
        self.epsilon = 0.1
        self.gamma = 0.9
        # increase value and epoch to increase
        self.delta = 0.05
        self.m = 5000
        self.matrix = self.createMatrix()
        print(self.matrix)

    def createMatrix(self):
        filename = "Qtable.txt"
        matrix = {}
        if os.path.exists(filename):
            print('hehe')
        else:
            for i in itertools.product([' ', 'F', '1', '2', '3', '4', '5', '6'], repeat=49):
                temp = []
                temp.append([0 for i in range(49)]) # value for revealing the cell
                temp.append([0 for i in range(49)]) # value for placing a flag in the cell
                temp.append(0)                      # value for choosing this state
                matrix.update({i: temp})
        return matrix

a = agent()