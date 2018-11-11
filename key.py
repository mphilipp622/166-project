import random
import board

class Key:
	def __init__(self, x, y, xmin, xmax, ymin, ymax):
		self.x = x
		self.y = y
		self.xmin = xmin
		self.xmax = xmax
		self.ymin = ymin
		self.ymax = ymax
		self.direction = None
		
	def move(self):
		myMoves = ["Left", "Right", "Up", "Down"]
		if ((self.x == self.xmin and self.direction == "Left") or (board.tiles(self.x-1, self.y).isWall() and self.direction == "Left")):
			myMoves.remove("Left")
		if ((self.x == self.xmax and self.direction == "Right") or (board.tiles(self.x+1, self.y).isWall() and self.direction == "Right")):
			myMoves.remove("Right")
		if ((self.y == self.ymin and self.direction == "Up") or (board.tiles(self.y-1, self.y).isWall() and self.direction == "Up")):
			myMoves.remove("Up")
		if ((self.y == self.ymax and self.direction == "Down") or (board.tiles(self.y+1, self.y).isWall() and self.directon == "Down")):
			myMoves.remove("Down")
			
		if (random.randint(0, 5) % 3 == 0)
			if self.direction in myMoves:
				myMoves.remove(self.direction)
			random.choice(myMoves)