import random
import objects

class Key:
    def __init__(self, x, y, xmin, xmax, ymin, ymax):
        self.x = x
        self.y = y
        self.xmin = xmin
        self.xmax = xmax
        self.ymin = ymin
        self.ymax = ymax
        self.direction = None
        self.acquired = False

    def go(self, direction):
        xMove = 0
        yMove = 0

        if direction=="Left":
            self.x -= 1
            xMove -= 1
        if direction=="Right":
            self.x += 1
            xMove += 1
        if direction=="Up":
            self.y -= 1
            yMove -= 1
        if direction=="Down":
            self.y += 1
            yMove += 1

        objects.graphics.moveKey(self, objects.board.size * xMove, objects.board.size * yMove)
        self.direction = direction
        
    def move(self, board):

        if self.acquired:
            # stop doing anything if key has been acquired
            return

        myMoves = ["Left", "Right", "Up", "Down"]

        if self.direction == None:
            self.direction = random.choice(myMoves)

        # rule out which actions we can take depending on current and next x, y positions
        if (self.x == self.xmin or self.x == 0 or board.tiles[self.x - 1][self.y].isNotValidKeyTile()):
            myMoves.remove("Left")
        if (self.x == self.xmax or self.x == board.width - 1 or board.tiles[self.x+1][self.y].isNotValidKeyTile()):
            myMoves.remove("Right")
        if (self.y == self.ymin or self.y == 0 or board.tiles[self.x][self.y-1].isNotValidKeyTile()):
            myMoves.remove("Up")
        if (self.y == self.ymax or self.y == board.height - 1 or board.tiles[self.x][self.y+1].isNotValidKeyTile()):
            myMoves.remove("Down")
        
        if len(myMoves) == 0:
            return
            
        board.tiles[self.x][self.y].key = False

        if (not(self.direction in myMoves) or (random.randint(0, 5) % 3 == 0)):
            if self.direction in myMoves and len(myMoves) > 1: # check the length to ensure we will have a move to make after removing
                myMoves.remove(self.direction)
            
            choice = random.choice(myMoves)
            self.go(choice)
        else:
            self.go(self.direction)
            
        board.tiles[self.x][self.y].key = True