from graphics import drawLine

class Player:
    def __init__(self, newX, newY, newBoard):
        self.x = newX
        self.y = newY
        self.size = 35
        self.board = newBoard

    def move(self, event, newDirection):

        # set the direction vector for the player movement
        xDirection = 0
        yDirection = 0

        if newDirection == "Down":
            yDirection = 1
        elif newDirection == "Up":
            yDirection = -1
        elif newDirection == "Right":
            xDirection = 1
        elif newDirection == "Left":
            xDirection = -1

        #initial x and y positions
        x0 = self.x * self.size + self.size / 2
        y0 = self.y * self.size + self.size / 2

        if yDirection != 0:
            while ((self.y - 1 >= 0) and (self.board[self.y + yDirection][self.x] != 1)):
                self.y += yDirection
                self.canvas.move(p, 0, -self.size)
        elif xDirection != 0:
            while ((self.x-1 >= 0) and (self.board[self.y][self.x + xDirection] != 1)):
                self.x += xDirection
                self.canvas.move(p, -self.size, 0)

        #x and y positions after movement
        x1 = self.x * self.size + self.size / 2
        x2 = self.y * self.size + self.size / 2

        drawLine(x0, y0, x1, y1)