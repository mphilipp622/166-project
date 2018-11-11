import random

class Key:
	def __init__(self, x, y, xmin, xmax, ymin, ymax):
		self.x = x
		self.y = y
		self.xmin = xmin
		self.xmax = xmax
		self.ymin = ymin
		self.ymax = ymax
		self.direction = None

	def go(self, direction):
		if direction=="Left":
			self.x -= 1
		if direction=="Right":
			self.x += 1
		if direction=="Up":
			self.y -= 1
		if direction=="Down":
			self.y += 1
		
	def move(self, board):
		print(str(self.x) + " by " + str(self.y) + "\n")
		board.tiles[self.x][self.y].key = False
		myMoves = ["Left", "Right", "Up", "Down"]
		if self.direction == None:
			self.direction = random.choice(myMoves)
		if ((self.x == self.xmin) or (self.x-1 > 0 and board.tiles[self.x-1][self.y].isWall() and self.direction == "Left")):
			myMoves.remove("Left")
		if ((self.x == self.xmax) or (self.x+1 < board.width-1 and board.tiles[self.x+1][self.y].isWall() and self.direction == "Right")):
			myMoves.remove("Right")
		if ((self.y == self.ymin) or (self.y-1 > 0 and board.tiles[self.x][self.y-1].isWall() and self.direction == "Up")):
			myMoves.remove("Up")
		if ((self.y == self.ymax) or (self.y+1 < board.height-1 and board.tiles[self.x][self.y+1].isWall() and self.direction == "Down")):
			myMoves.remove("Down")
			
		if (not(self.direction in myMoves) or (random.randint(0, 5) % 3 == 0)):
			if self.direction in myMoves:
				myMoves.remove(self.direction)
			choice = random.choice(myMoves)
			self.go(choice)
		else:
			self.go(self.direction)
		board.tiles[self.x][self.y].key = True