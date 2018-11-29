import objects
import random
import time
import main
import copy

class Player:

	def __init__(self, newX, newY):
		self.x = newX   # x position of player
		self.y = newY   # y position of player
		self.size = int(objects.board.size / 1.75)
		self.keyCount = 0
		self.overrideAction = None

	def getActionVector(self, board):
	    # helper function called by aiMove() to get a vector of valid directions from the player's current position.

	    validMoves = ["Left", "Right", "Up", "Down", "Stay"]

		# rule out which actions we can take depending on current and next x, y positions. Based on implementation in key.py
	    if self.x == 0 or board.tiles[self.x-1][self.y].isWall():
		    validMoves.remove("Left")
	    if self.x == board.width - 1 or board.tiles[self.x+1][self.y].isWall():
	    	validMoves.remove("Right")
	    if self.y == 0 or board.tiles[self.x][self.y-1].isWall():
	    	validMoves.remove("Up")
	    if self.y == board.height - 1 or board.tiles[self.x][self.y+1].isWall():
	        validMoves.remove("Down")

	    return validMoves


	def aiQMove(self, action, board, graphics):
		# will perform movement and track rewards as it moves. Will then tell the qLearn object what reward it got

		boardSize = board.size  # grab the board size of the current board
		totalReward = 0
		hasDied = False
		resultingKeyPositionList = copy.deepcopy(board.keys)

		# set the direction vector for the player movement based on the newDirection variable
		xDirection = 0
		yDirection = 0

		# note that the x, y origin is at the top-left, which is why UP is -1 in the y direction.
		xDirection = self.getXDirection(action)
		yDirection = self.getYDirection(action)

		#initial x and y positions
		x0 = self.x * boardSize + boardSize / 2
		y0 = self.y * boardSize + boardSize / 2

		objects.board.tiles[self.x][self.y].player = False
		resultingKeyPositionList = copy.deepcopy(objects.qLearn.currentState.keyPositions) # this list will be updated if keys are acquired taking this action

		while((yDirection != 0 or xDirection != 0) 
		and (self.y + yDirection >= 0 and self.y + yDirection < objects.board.height)
		and (self.x + xDirection >= 0 and self.x + xDirection < objects.board.width)
		and not (objects.board.tiles[self.x + xDirection][self.y + yDirection].isWall())):
			self.x += xDirection
			self.y += yDirection

			if hasDied is False:
				graphics.moveCanvas(boardSize * xDirection, boardSize * yDirection)

			if board.tiles[self.x][self.y].hasKey():
				self.keyCount += 1
				board.removeKey(self.x, self.y)
				totalReward += 10

			if board.tiles[self.x][self.y].isLava():
				hasDied = True
				totalReward -= 1000
				
			if objects.board.tiles[self.x][self.y].isWormhole():
				wormhole = objects.board.tiles[self.x][self.y]
				x1 = self.x * boardSize + boardSize / 2
				x2 = self.y * boardSize + boardSize / 2

				# render the line behind player
				graphics.drawLine(x0, y0, x1, x2)
				self.x = wormhole.exit.exitX
				self.y = wormhole.exit.exitY
				action = wormhole.translateDirection(action)
				xDirection = self.getXDirection(action)
				yDirection = self.getYDirection(action)
				objects.graphics.teleportPlayer(self.x, self.y)
				x0 = self.x * boardSize + boardSize / 2
				y0 = self.y * boardSize + boardSize / 2
				continue

			# objects.graphics.moveCanvas(boardSize * xDirection, boardSize * yDirection)

		objects.board.tiles[self.x][self.y].player = True

		x1 = self.x * boardSize + boardSize / 2
		x2 = self.y * boardSize + boardSize / 2

		# render the line behind player
		graphics.drawLine(x0, y0, x1, x2)

		if board.tiles[self.x][self.y].isExit() and self.keyCount >= board.exitKeysRequired:
			print("Player Wins")
			totalReward += 100
			objects.qLearn.updateState(action, totalReward)
			objects.qLearn.numberOfWins += 1.0
			time.sleep(0.1)
			main.restart()
			return

		if hasDied is True:
			print("Player Died")
			objects.qLearn.updateState(action, totalReward)
			time.sleep(0.1)
			main.restart()
		else:
			objects.qLearn.updateState(action, totalReward)

	def aiMove(self, action, board, graphics):
		# This function will be run in main.py main() function in the game loop.
		# board and graphics are the same as objects.board and objects.graphics.
		# They're being passed to this function from main.py main() function

		boardSize = board.size  # grab the board size of the current board

		# set the direction vector for the player movement based on the newDirection variable
		xDirection = 0
		yDirection = 0

		# note that the x, y origin is at the top-left, which is why UP is -1 in the y direction.
		xDirection = self.getXDirection(action)
		yDirection = self.getYDirection(action)

		#initial x and y positions
		x0 = self.x * boardSize + boardSize / 2
		y0 = self.y * boardSize + boardSize / 2

		objects.board.tiles[self.x][self.y].player = False

		while((yDirection != 0 or xDirection != 0) 
		and (self.y + yDirection >= 0 and self.y + yDirection < objects.board.height)
		and (self.x + xDirection >= 0 and self.x + xDirection < objects.board.width)
		and not (objects.board.tiles[self.x + xDirection][self.y + yDirection].isWall())):
			self.x += xDirection
			self.y += yDirection

			if board.tiles[self.x][self.y].hasKey():
				self.keyCount += 1
				board.removeKey(self.x, self.y)

			if board.tiles[self.x][self.y].isLava():
				print("Player Died")
				time.sleep(0.1)
				main.restart()

			if objects.board.tiles[self.x][self.y].isWormhole():
				wormhole = objects.board.tiles[self.x][self.y]
				x1 = self.x * boardSize + boardSize / 2
				x2 = self.y * boardSize + boardSize / 2

				# render the line behind player
				graphics.drawLine(x0, y0, x1, x2)
				self.x = wormhole.exit.exitX
				self.y = wormhole.exit.exitY
				action = wormhole.translateDirection(action)
				xDirection = self.getXDirection(action)
				yDirection = self.getYDirection(action)
				objects.graphics.teleportPlayer(self.x, self.y)
				x0 = self.x * boardSize + boardSize / 2
				y0 = self.y * boardSize + boardSize / 2
				continue

			objects.graphics.moveCanvas(boardSize * xDirection, boardSize * yDirection)

		objects.board.tiles[self.x][self.y].player = True

		#x and y positions after movement
		x1 = self.x * boardSize + boardSize / 2
		x2 = self.y * boardSize + boardSize / 2

		# render the line behind player
		graphics.drawLine(x0, y0, x1, x2)

		if board.tiles[self.x][self.y].isExit() and self.keyCount >= board.exitKeysRequired:
			print("Player Wins")
			time.sleep(0.1)
			main.restart()


	def move(self, event, newDirection):
		# pass argument None for event if you aren't using keyboard to move player. E.G: move(None, "Up")

		boardSize = objects.board.size  # grab the board size of the current board

		# set the direction vector for the player movement based on the newDirection variable
		xDirection = self.getXDirection(newDirection)
		yDirection = self.getYDirection(newDirection)

		# if self.overrideAction != None:
		# 	newDirection = self.overrideAction
		# 	self.overrideAction = None

		#initial x and y positions
		x0 = self.x * boardSize + boardSize / 2
		y0 = self.y * boardSize + boardSize / 2

		while((yDirection != 0 or xDirection != 0) 
		and (self.y + yDirection >= 0 and self.y + yDirection < objects.board.height)
		and (self.x + xDirection >= 0 and self.x + xDirection < objects.board.width)
		and not (objects.board.tiles[self.x + xDirection][self.y + yDirection].isWall())):
			self.x += xDirection
			self.y += yDirection

			if objects.board.tiles[self.x][self.y].isWormhole():
				wormhole = objects.board.tiles[self.x][self.y]
				x1 = self.x * boardSize + boardSize / 2
				x2 = self.y * boardSize + boardSize / 2

				# render the line behind player
				objects.graphics.drawLine(x0, y0, x1, x2)
				self.x = wormhole.exit.exitX
				self.y = wormhole.exit.exitY
				newDirection = wormhole.translateDirection(newDirection)
				xDirection = self.getXDirection(newDirection)
				yDirection = self.getYDirection(newDirection)
				objects.graphics.teleportPlayer(self.x, self.y)
				x0 = self.x * boardSize + boardSize / 2
				y0 = self.y * boardSize + boardSize / 2
				continue

			objects.graphics.moveCanvas(boardSize * xDirection, boardSize * yDirection)


		#x and y positions after movement
		x1 = self.x * boardSize + boardSize / 2
		x2 = self.y * boardSize + boardSize / 2

		# render the line behind player
		objects.graphics.drawLine(x0, y0, x1, x2)

	def getXDirection(self, newDirection):
		if newDirection == "Right":
			return 1
		elif newDirection == "Left":
			return -1
		
		return 0

	def getYDirection(self, newDirection):
		if newDirection == "Down":
			return 1
		elif newDirection == "Up":
			return -1

		return 0