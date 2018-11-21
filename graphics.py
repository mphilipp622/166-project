import keyboard
import time
import objects
import key

try:
    from tkinter import *   # handles python 3 compiler
except ImportError:
    from Tkinter import *   # handles python 2 compiler

class Graphics:

    def __init__(self):
        self.root = Tk()                     #This creates a window, but it won't show up
        self.root.wm_title("CSCI 166 Project       by: Joshua Holland") #Makes the title that will appear in the top left
        self.root.geometry("%dx%d+%d+%d" % (objects.board.width * objects.board.size, objects.board.height * objects.board.size, 130, 100))
        self.playerGraphic = None
        self.job = None
        self.canvas = Canvas(self.root, width = objects.board.width * objects.board.size, height= objects.board.height * objects.board.size, background = 'black')

        # initialize keyboard listeners and assign them to player movement function
        self.root.bind("<Up>", lambda event: objects.player.move(event, newDirection = "Up"))
        self.root.bind("<Down>", lambda event: objects.player.move(event, newDirection = "Down"))
        self.root.bind("<Left>", lambda event: objects.player.move(event, newDirection = "Left"))
        self.root.bind("<Right>", lambda event: objects.player.move(event, newDirection = "Right"))

        self.canvas.pack()

        self.keys = dict()

        # self.initializeGraphics()
        # self.keys = dict()
        # self.wormholes = dict()

    def drawLine(self, x0, y0, x1, x2):
        # renders line behind player after movement
        line = self.canvas.create_line(x0, y0, x1, x2, width = 3, fill='red')
        self.root.update()
        time.sleep(.2)
        self.canvas.delete(line)

    def moveCanvas(self, xAmount, yAmount):
        # Called from player.move()
        self.canvas.move(self.playerGraphic, xAmount, yAmount)

    def moveKey(self, key, xAmount, yAmount):
        self.canvas.move(self.keys[key], xAmount, yAmount)

    def removeKey(self, key):
        self.canvas.delete(self.keys[key])
        del self.keys[key]

    def updateBoard(self):
        # redraw the board
        self.canvas.delete("all")

        for i in range(objects.board.width):
            for j in range(objects.board.height):
                xpos = i * objects.board.size
                ypos = j * objects.board.size
                rect = self.canvas.create_rectangle(xpos, ypos, xpos + objects.board.size, ypos + objects.board.size, fill='#FFF')

                if objects.board.tiles[i][j].isWall():
                    self.canvas.itemconfig(rect, fill='black')
                elif objects.board.tiles[i][j].isEmpty(): 
                    self.canvas.itemconfig(rect, fill='white')
                elif objects.board.tiles[i][j].isLava():
                    self.canvas.itemconfig(rect, fill='red')
                elif objects.board.tiles[i][j].isWormhole():
                    self.canvas.itemconfig(rect, fill='purple')
                elif objects.board.tiles[i][j].isWormholeExit():
                    self.canvas.itemconfig(rect, fill='green')
                elif objects.board.tiles[i][j].isExit():
                    self.canvas.itemconfig(rect, fill = "gold")

    def drawPlayer(self):
        boardSize = objects.board.size
        playerSize = objects.player.size
        
        if self.playerGraphic:
            del self.playerGraphic

        self.playerGraphic = self.canvas.create_oval(objects.player.x *boardSize + (boardSize - playerSize) / 2,
													objects.player.y*boardSize + (boardSize - playerSize) / 2, 
													objects.player.x*boardSize + boardSize - (boardSize - playerSize) / 2, 
													objects.player.y*boardSize + boardSize - (boardSize - playerSize) / 2, 
													fill='red')
    
    
    def drawKeys(self):
        boardSize = objects.board.size
        playerSize = objects.player.size

        self.keys.clear()   # clear any keys so that we can reset graphics without closing program.

        for key in objects.board.keys:
            self.keys[key] = self.canvas.create_oval(key.x *boardSize + (boardSize - playerSize) / 2,
													key.y*boardSize + (boardSize - playerSize) / 2, 
													key.x*boardSize + boardSize - (boardSize - playerSize) / 2, 
													key.y*boardSize + boardSize - (boardSize - playerSize) / 2, 
													fill='yellow')

    def initializeGraphics(self):
        # this function initializes the graphics and starts tkinter's main loop.
        # it begins concurrent execution of main() inside main.py
        # This is called from start() in main.py
        import main

        self.updateBoard()
        self.drawPlayer()
        self.drawKeys()
        self.job = self.root.after(10, main.main) # after() allows us to say "after 10 ms, run main()". This allows us to make a game loop inside main.py
        self.root.mainloop()

    def redrawBoard(self):
        import main

        self.root.after_cancel(self.job)
        self.updateBoard()
        self.drawPlayer()
        self.drawKeys()
        self.job = self.root.after(100, main.main)
        self.root.mainloop()

    def quit(self):
        self.root.destroy()