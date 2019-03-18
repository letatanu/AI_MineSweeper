from MineSweeper import *
from Agent import *



def main():
    game = MineSweeper()
    agent = Agent(gameObject=game)
    epsilon = 0.1
    delta = 0.01
    numberOfEpoch = 10000
    m = numberOfEpoch*delta
    epoch = 1
    # running for xxx epochs
    while 1:
        if epsilon > 1:
            break

        if epoch % m == 0:
            epsilon = epsilon + delta
        r = agent.train(epsilon)

        # run an epoch
        while r != -1:
            r = agent.train(epsilon)
        epoch = epoch+1

    print(epoch)

if __name__ == '__main__':
    main()