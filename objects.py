import player
import board
import graphics
import sys
import state
import mdp as mdpLibrary

# This file is used by main, player, and board for accessing instances of these classes for cross communication

if len(sys.argv) > 1:
    # boardConstructor(height, width, tileSize)
    board = board.Board(sys.argv[1])
else:
    print("error: no level json argument given")
    exit()

#playerConstructor(startingXPos, startingYPos)
player = player.Player(board.playerPosition[0], board.playerPosition[1])

mdp = mdpLibrary.MDP(state.State((player.x, player.y), [(key.x, key.y) for key in board.keys], None))

# currentState = state.State(player, None, board.keys)    # tracks the current state of the game.

graphics = graphics.Graphics()