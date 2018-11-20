import player as playerLibrary
import board as boardLibrary
import graphics as graphicsLibrary
import sys
import state
import mdp as mdpLibrary
import qLearning as qLearningLibrary

# This file is used by main, player, and board for accessing instances of these classes for cross communication

def initialize():
    global board, player, mdp, graphics

    if len(sys.argv) > 2:
        if "json" not in sys.argv[1]:
            print("error: level json argument must be first argument")
            exit()
        if sys.argv[2] != 'v' and sys.argv[2] != 'q':
            print("error: AI algorithm type not specified. Please use 'v' for value iteration or 'q' for q-learning")
            exit()

        # boardConstructor(height, width, tileSize)
        board = boardLibrary.Board(sys.argv[1])

        #playerConstructor(startingXPos, startingYPos)
        player = playerLibrary.Player(board.playerPosition[0], board.playerPosition[1])

        mdp = mdpLibrary.MDP(state.State((player.x, player.y), [(key.x, key.y) for key in board.keys], None))

        # currentState = state.State(player, None, board.keys)    # tracks the current state of the game.

        graphics = graphicsLibrary.Graphics()

        # if sys.argv[2] == 'v':
        #     ai = mdpLibrary.MDP(state.State((player.x, player.y), [(key.x, key.y) for key in board.keys], None))
        # elif sys.argv[2] == 'q':
        #     ai = qLearningLibrary.QLearn(state.State((player.x, player.y), [(key.x, key.y) for key in board.keys], None))
    else:
        print("error: not enough arguments provided. Provide level json file followed by string 'v' or 'q' for value iteration or q-learning respectively")
        exit()

def restart():
    # boardConstructor(height, width, tileSize)
    board = boardLibrary.Board(sys.argv[1])

    #playerConstructor(startingXPos, startingYPos)
    player = playerLibrary.Player(board.playerPosition[0], board.playerPosition[1])

    mdp.updateCurrentState(player, board.keys, None)
    graphics = graphicsLibrary.Graphics()