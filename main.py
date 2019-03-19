from MineSweeper import *
from Agent import *
import pickle
import matplotlib.pyplot as plt
gridSize = 7
numberOfMines = 5


def main():
    test()
    # train()

def test():
    # create a new game
    cgridSize = 7
    cnumberOfMines = 5
    numberOfGames = 1000
    countOfWinGame = 0
    for i in range(numberOfGames):
        ####################Playing a game ######################

        # initializing a minesweeper game
        game = MineSweeper(gridsize=cgridSize, numberOfMines=cnumberOfMines)
        # reading trained q_matrix
        q_matrix = pickle.load(open('Q_Matrix%d_%d.p' % (gridSize, numberOfMines), "rb"))
        #initializing an agent for that q_matrix and game
        agent = Agent(Q_Matrix=q_matrix, gameObject=game)
        r = 0
        #showing current grid of game
        game.showgrid(game.currgrid)
        while r!=-1 and r !=1:
            # agent returns its decision for the action
            loc = agent.play() # get an action for current grid
            print(loc)
            # passing the location to game
            r = game.playgame(loc) # doing an action
       #############################################################################


            if r == 1:
                countOfWinGame = countOfWinGame + 1

    print('%d win games over %d games'%(countOfWinGame, numberOfGames))

def train():
    game = MineSweeper(gridsize=gridSize, numberOfMines=numberOfMines)
    agent = Agent(gameObject=game)
    epsilon = 0.1
    delta = 0.01
    numberOfEpoch = 100000
    m = numberOfEpoch * delta
    epoch = 1
    # running for xxx epochs
    scores = []
    while 1:
        if epsilon > 1:
            break

        if epoch % m == 0:
            epsilon = epsilon + delta
        r = agent.train(epsilon)

        # run an epoch
        # each correct step, score = 1
        score = 0
        if r != -1 and r != 1:
            while 1:
                score = score + 1
                r = agent.train(epsilon)
                # a win game gives a score of 3
                if r == 1:
                    score = score + 3
                    break
                if r == -1:
                    break
        scores.append(score)
        epoch = epoch + 1

    # take average for every m elements
    m = int(m)
    i = 0
    finalScores = []
    tmpScore = []
    for score in scores:
        i = i + 1
        tmpScore.append(score)
        if i % m == 0:
            finalScores.append(np.mean(np.array(tmpScore)))
            tmpScore = []
    print(epoch)
    plt.plot(finalScores)
    plt.title("MineSweeper of %d x %d with %d mines" % (gridSize, gridSize, numberOfMines))
    plt.xlabel("%d X Epochs" % int(m))
    plt.ylabel("Score")
    plt.savefig('player%d_%d.png' % (gridSize, numberOfMines))
    pickle.dump(agent.Q_Matrix, open('Q_Matrix%d_%d.p' % (gridSize, numberOfMines), "wb"))

if __name__ == '__main__':
    main()