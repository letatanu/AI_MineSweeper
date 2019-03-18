import random
from string import ascii_lowercase
import re

class MineSweeperTrain(object):
    '''a minesweeper game for agent training'''

    def __init__(self):
        self.gridsize = 20
        self.numberofmines = 100
        self.currgrid = [[' ' for i in range(self.gridsize)] for i in range(self.gridsize)]
        self.grid = []
        self.flags = []
        self.mines = []
        self.available = [(a, b) for a in range(self.gridsize) for b in range(self.gridsize)]   # available actions
        self.currgrid = [[' ' for i in range(self.gridsize)] for i in range(self.gridsize)]

    def setupgrid(self, start):
        emptygrid = [['0' for i in range(self.gridsize)] for i in range(self.gridsize)]

        self.getmines(emptygrid, start)

        for i, j in self.mines:
            emptygrid[i][j] = 'X'

        self.grid = self.getnumbers(emptygrid)

    def getmines(self, grid, start):
        neighbors = self.getneighbors(grid, *start)

        for i in range(self.numberofmines):
            cell = self.getrandomcell(grid)
            while cell == start or cell in self.mines or cell in neighbors:
                cell = self.getrandomcell(grid)
            self.mines.append(cell)
        
    def getnumbers(self, grid):
        for rowno, row in enumerate(grid):
            for colno, cell in enumerate(row):
                if cell != 'X':
                    # gets the values of the neighbors
                    values = [grid[r][c] for r, c in self.getneighbors(grid, rowno, colno)]
                    # counts how many are mines
                    grid[rowno][colno] = str(values.count('X'))

        return grid

    def getneighbors(self, grid, rowno, colno):
        neighbors = []

        for i in range(-1, 2):
            for j in range(-1, 2):
                if i == 0 and j == 0:
                    continue
                elif -1 < (rowno + i) < self.gridsize and -1 < (colno + j) < self.gridsize:
                    neighbors.append((rowno + i, colno + j))

        return neighbors

    def getrandomcell(self, grid):
        a = random.randint(0, self.gridsize - 1)
        b = random.randint(0, self.gridsize - 1)

        return (a, b)

    def showcells(self, rowno, colno):
        if self.currgrid[rowno][colno] != ' ':
            return
        self.available.remove((rowno, colno))
        self.currgrid[rowno][colno] = self.grid[rowno][colno]

        if self.grid[rowno][colno] == '0':
            for r, c in self.getneighbors(self.grid, rowno, colno):
                self.showcells(r, c)

    def check_win(self):
        '''win -> True'''
        # the old one
        # if set(self.flags) == set(self.mines):
            # return True
        if set(self.available) == set(self.mines):
            return True
        return False

    def play(self, step):
        '''
        returns the current state, and a return value indicating whether the game is over:
        triggered a mine -> -1, win -> 1, otherwise -> 0
        '''

        rowno, colno = step
        currcell = self.currgrid[rowno][colno]
        returnVal = 0

        if not self.grid:
            self.setupgrid(step)

        if self.grid[rowno][colno] == 'X':
            returnVal = -1
        
        elif currcell == ' ':
            self.showcells(rowno, colno)

        if self.check_win():
            returnVal = 1

        return self.currgrid, returnVal