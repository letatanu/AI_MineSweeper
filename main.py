from MineSweeper import *
from Agent import *
import pickle
import matplotlib.pyplot as plt

def main():
    gridSize = 5
    numberOfMines = 3
    game = MineSweeper(gridsize=gridSize, numberOfMines=numberOfMines)
    agent = Agent(gameObject=game)
    epsilon = 0.1
    delta = 0.01
    numberOfEpoch = 100000
    m = numberOfEpoch*delta
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
        while r != -1 and r != 1:
            score = score + 1
            r = agent.train(epsilon)
            # a win game gives a score of 3
            if r == 1:
                score = score + 3
        scores.append(score)
        epoch = epoch+1

    # take average for every m elements
    scores = np.mean(np.array(scores).reshape(-1, int(m)), axis=1)

    print(epoch)
    plt.plot(scores)
    plt.xlabel("%d X Epochs"%int(m))
    plt.ylabel("Score")
    plt.savefig('player1.png')
    pickle.dump(agent.Q_Matrix, open('Q_Matrix5.p', "wb"))

if __name__ == '__main__':
    main()