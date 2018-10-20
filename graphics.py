import keyboard
import time
import objects

try:
    from tkinter import *   # handles python 3 compiler
except ImportError:
    from Tkinter import *   # handles python 2 compiler

class Graphics:

    def __init__(self):
        self.root = Tk()                     #This creates a window, but it won't show up
        self.root.wm_title("CSCI 166 Project       by: Joshua Holland") #Makes the title that will appear in the top left
        self.root.geometry("%dx%d+%d+%d" % (objects.board.width * objects.board.size, objects.board.height * objects.board.size, 130, 100))

        self.canvas = Canvas(self.root, width = objects.board.width * objects.board.size, height= objects.board.height * objects.board.size, background = 'black')

        # initialize keyboard listeners and assign them to player movement function
        self.root.bind("<Up>", lambda event: objects.player.move(event, newDirection = "Up"))
        self.root.bind("<Down>", lambda event: objects.player.move(event, newDirection = "Down"))
        self.root.bind("<Left>", lambda event: objects.player.move(event, newDirection = "Left"))
        self.root.bind("<Right>", lambda event: objects.player.move(event, newDirection = "Right"))

        self.canvas.pack()

    def drawLine(self, x0, y0, x1, x2):
        # renders line behind player after movement
        line = self.canvas.create_line(x0, y0, x1, x2, width = 3, fill='red')
        self.root.update()
        time.sleep(.2)
        self.canvas.delete(line)

    def moveCanvas(self, xAmount, yAmount):
        # Called from player.move()
        self.canvas.move(self.p, xAmount, yAmount)

    def updateBoard(self):
        # redraw the board
        self.canvas.delete("all")

        for i in range(objects.board.height):
            for j in range(objects.board.width):
                xpos = j * objects.board.size
                ypos = i * objects.board.size
                rect = self.canvas.create_rectangle(xpos, ypos, xpos + objects.board.size, ypos + objects.board.size, fill='#FFF')

                if objects.board.tiles[i][j].isWall():
                    self.canvas.itemconfig(rect, fill='black')
                else: 
                    self.canvas.itemconfig(rect, fill='white')

    def drawPlayer(self):
        boardSize = objects.board.size
        playerSize = objects.player.size

        self.p = self.canvas.create_oval(0 + (boardSize - playerSize) / 2,
                                        0 + (boardSize - playerSize) / 2, 
                                        0 + boardSize - (boardSize - playerSize) / 2, 
                                        0 + boardSize - (boardSize - playerSize) / 2, 
                                        fill='red')

    def updateCanvas(self):
        # main loop that's called from main
        self.updateBoard()
        self.drawPlayer()
        self.root.mainloop()