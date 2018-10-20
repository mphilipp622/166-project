import player
import board
import graphics

# This file is used by main, player, and board for accessing instances of these classes for cross communication

# boardConstructor(height, width, tileSize)
board = board.Board(10, 15, 60)

#playerConstructor(startingXPos, startingYPos)
player = player.Player(0, 0)

graphics = graphics.Graphics()