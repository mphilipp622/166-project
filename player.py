import objects

class Player:
    def __init__(self, newX, newY):
        self.x = newX   # x position of player
        self.y = newY   # y position of player
        self.size = 35

    def move(self, event, newDirection):
        # pass argument None for event if you aren't using keyboard to move player. E.G: move(None, "Up")

        boardSize = objects.board.size  # grab the board size of the current board

        # set the direction vector for the player movement based on the newDirection variable
        xDirection = 0
        yDirection = 0

        # note that the x, y origin is at the top-left, which is why UP is -1 in the y direction.
        if newDirection == "Down":
            yDirection = 1
        elif newDirection == "Up":
            yDirection = -1
        elif newDirection == "Right":
            xDirection = 1
        elif newDirection == "Left":
            xDirection = -1

        #initial x and y positions
        x0 = self.x * boardSize + boardSize / 2
        y0 = self.y * boardSize + boardSize / 2

        # handle movement bounds checking. If player hits a wall or ends up on a perimeter tile, stop moving. 
        # Otherwise, keep moving and update graphics.
        if yDirection != 0:
            while ((self.y + yDirection >= 0 and self.y + yDirection < objects.board.height) and 
            not (objects.board.tiles[self.x][self.y + yDirection].isWall())):
                self.y += yDirection
                objects.graphics.moveCanvas(0, boardSize * yDirection)
                
        elif xDirection != 0:
            while ((self.x + xDirection >= 0 and self.x + xDirection < objects.board.width) and 
            not (objects.board.tiles[self.x + xDirection][self.y].isWall())):
                self.x += xDirection
                objects.graphics.moveCanvas(boardSize * xDirection, 0)

        #x and y positions after movement
        x1 = self.x * boardSize + boardSize / 2
        x2 = self.y * boardSize + boardSize / 2

        # render the line behind player
        objects.graphics.drawLine(x0, y0, x1, x2)