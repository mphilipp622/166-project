import player
import board
import graphics
import sys

# This file is used by main, player, and board for accessing instances of these classes for cross communication

if len(sys.argv) > 1:
    # boardConstructor(height, width, tileSize)
    board = board.Board(sys.argv[1])
else:
    print("error: no level json argument given")
    exit()

#playerConstructor(startingXPos, startingYPos)
player = player.Player(board.playerPosition[1], board.playerPosition[0])

graphics = graphics.Graphics()