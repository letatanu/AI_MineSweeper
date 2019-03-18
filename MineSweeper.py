"""A command line version of Minesweeper"""
import random
import numpy as np
import time
from string import ascii_lowercase

class MineSweeper:
    def __init__(self, gridsize = 7, numberOfMines = 10):
        self.gridsize = gridsize
        self.numberofmines = numberOfMines

        self.currgrid = [['E' for i in range(gridsize)] for i in range(gridsize)]

        self.grid = []
        self.starttime = 0

    def setupgrid(self,gridsize, start, numberofmines):
        emptygrid = [['0' for i in range(gridsize)] for i in range(gridsize)]

        mines = self.getmines(emptygrid, start, numberofmines)

        for i, j in mines:
            emptygrid[i][j] = 'X'

        grid = self.getnumbers(emptygrid)

        return (grid, mines)


    def showgrid(self, grid):
        gridsize = len(grid)

        horizontal = '   ' + (4 * gridsize * '-') + '-'

        # Print top column letters
        toplabel = '     '

        for i in ascii_lowercase[:gridsize]:
            toplabel = toplabel + i + '   '

        print(toplabel + '\n' + horizontal)

        # Print left row numbers
        for idx, i in enumerate(grid):
            row = '{0:2} |'.format(idx + 1)

            for j in i:
                if j == 'E':
                    j = ' '
                row = row + ' ' + j + ' |'

            print(row + '\n' + horizontal)

        print('')


    def getrandomcell(self, grid):
        gridsize = len(grid)

        a = random.randint(0, gridsize - 1)
        b = random.randint(0, gridsize - 1)

        return (a, b)


    def getneighbors(self, grid, rowno, colno):
        gridsize = len(grid)
        neighbors = []

        for i in range(-1, 2):
            for j in range(-1, 2):
                if i == 0 and j == 0:
                    continue
                elif -1 < (rowno + i) < gridsize and -1 < (colno + j) < gridsize:
                    neighbors.append((rowno + i, colno + j))

        return neighbors


    def getmines(self, grid, start, numberofmines):
        mines = []
        neighbors = self.getneighbors(grid, *start)

        for i in range(numberofmines):
            cell = self.getrandomcell(grid)
            while cell == start or cell in mines or cell in neighbors:
                cell = self.getrandomcell(grid)
            mines.append(cell)

        return mines


    def getnumbers(self, grid):
        for rowno, row in enumerate(grid):
            for colno, cell in enumerate(row):
                if cell != 'X':
                    # Gets the values of the neighbors
                    values = [grid[r][c] for r, c in self.getneighbors(grid,
                                                                  rowno, colno)]

                    # Counts how many are mines
                    grid[rowno][colno] = str(values.count('X'))

        return grid


    def showcells(self, grid, currgrid, rowno, colno):
        # Exit function if the cell was already shown
        if currgrid[rowno][colno] != 'E':
            return

        # Show current cell
        currgrid[rowno][colno] = grid[rowno][colno]

        # Get the neighbors if the cell is empty
        if grid[rowno][colno] == '0':
            for r, c in self.getneighbors(grid, rowno, colno):
                # Repeat function for each neighbor that doesn't have a flag
                self.showcells(grid, currgrid, r, c)


    def playgame(self, loc):
        if not loc is None:
            print('\n\n')
            rowno, colno = loc
            currcell = self.currgrid[rowno][colno]
            # flag = result['flag']

            if not self.grid:
                self.grid, mines = self.setupgrid(self.gridsize, loc, self.numberofmines)
            if not self.starttime:
                self.starttime = time.time()

            if self.grid[rowno][colno] == 'X':
                print('Game Over\n')
                self.showgrid(self.grid)
                return -1

            elif currcell == 'E':
                self.showcells(self.grid, self.currgrid, rowno, colno)
                self.showgrid(self.currgrid)
            else:
                print(loc)
                print("That cell is already shown")
                return 0

            currGrid = np.array(self.currgrid)
            minesleft = self.numberofmines - len(currGrid[currGrid=='E'])

            if minesleft == 0:
                minutes, seconds = divmod(int(time.time() - self.starttime), 60)
                print(
                    'You Win. '
                    'It took you {} minutes and {} seconds.\n'.format(minutes,
                                                                      seconds))
                self.showgrid(self.grid)
                return 1
        return 0
