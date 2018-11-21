import objects
import random
import time
import main

class Player:
    def __init__(self, newX, newY):
        self.x = newX   # x position of player
        self.y = newY   # y position of player
        self.size = objects.board.size / 1.75
        self.keyCount = 0

    # def getActionVector(self, board):
    #     # helper function called by aiMove() to get a vector of valid directions from the player's current position.

    #     validMoves = ["Left", "Right", "Up", "Down", "Stay"]

	# 	# rule out which actions we can take depending on current and next x, y positions. Based on implementation in key.py
    #     if self.x == 0 or board.tiles[self.x-1][self.y].isWall():
	# 	    validMoves.remove("Left")
    #     if self.x == board.width - 1 or board.tiles[self.x+1][self.y].isWall():
    #     	validMoves.remove("Right")
    #     if self.y == 0 or board.tiles[self.x][self.y-1].isWall():
    #     	validMoves.remove("Up")
    #     if self.y == board.height - 1 or board.tiles[self.x][self.y+1].isWall():
    #         validMoves.remove("Down")

    #     return validMoves

    def aiQMove(self, action, board, graphics):
        

    def aiMove(self, action, board, graphics):
        # This function will be run in main.py main() function in the game loop.
        # board and graphics are the same as objects.board and objects.graphics. 
        # They're being passed to this function from main.py main() function

        boardSize = board.size  # grab the board size of the current board

        # set the direction vector for the player movement based on the newDirection variable
        xDirection = 0
        yDirection = 0

        # note that the x, y origin is at the top-left, which is why UP is -1 in the y direction.
        if action == "Down":
            yDirection = 1
        elif action == "Up":
            yDirection = -1
        elif action == "Right":
            xDirection = 1
        elif action == "Left":
            xDirection = -1

        #initial x and y positions
        x0 = self.x * boardSize + boardSize / 2
        y0 = self.y * boardSize + boardSize / 2

        objects.board.tiles[self.x][self.y].player = False
        # handle movement bounds checking. If player hits a wall or ends up on a perimeter tile, stop moving. 
        # Otherwise, keep moving and update graphics.
        if yDirection != 0:
            while ((self.y + yDirection >= 0 and self.y + yDirection < board.height) and 
            not (board.tiles[self.x][self.y + yDirection].isWall())):
                self.y += yDirection

                if board.tiles[self.x][self.y].hasKey():
                    self.keyCount += 1
                    board.removeKey(self.x, self.y)
                if board.tiles[self.x][self.y].isLava():
                    print("Player Died")
                    time.sleep(0.1)
                    main.restart()

                graphics.moveCanvas(0, boardSize * yDirection)
                
        elif xDirection != 0:
            while ((self.x + xDirection >= 0 and self.x + xDirection < board.width) and 
            not (board.tiles[self.x + xDirection][self.y].isWall())):
                self.x += xDirection

                if board.tiles[self.x][self.y].hasKey():
                    self.keyCount += 1
                    board.removeKey(self.x, self.y)
                if board.tiles[self.x][self.y].isLava():
                    print("Player Died")
                    time.sleep(0.1)
                    main.restart()
                    
                graphics.moveCanvas(boardSize * xDirection, 0)

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


    