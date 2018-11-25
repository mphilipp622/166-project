import keyboard
import time
import objects
import key

try:
    from tkinter import *   # handles python 3 compiler
except ImportError:
    from Tkinter import *   # handles python 2 compiler

from PIL import Image, ImageTk

class Graphics:

    def __init__(self):
        self.root = Tk()                     #This creates a window, but it won't show up
        self.root.wm_title("CSCI 166 Project       by: Joshua Holland") #Makes the title that will appear in the top left
        self.root.geometry("%dx%d+%d+%d" % (objects.board.width * objects.board.size, objects.board.height * objects.board.size, 130, 100))
        self.playerGraphic = None
        self.job = None
        self.canvas = Canvas(self.root, width = objects.board.width * objects.board.size, height= objects.board.height * objects.board.size)

        # initialize keyboard listeners and assign them to player movement function
        self.root.bind("<Up>", lambda event: objects.player.move(event, newDirection = "Up"))
        self.root.bind("<Down>", lambda event: objects.player.move(event, newDirection = "Down"))
        self.root.bind("<Left>", lambda event: objects.player.move(event, newDirection = "Left"))
        self.root.bind("<Right>", lambda event: objects.player.move(event, newDirection = "Right"))

        self.canvas.pack()

        self.keys = dict()      # stores keys of type key.id, which is integer, and returns a canvas opal object.

        # self.initializeGraphics()
        # self.keys = dict()
        # self.wormholes = dict()

    def drawBackground(self):
        self.canvas.pack(fill=BOTH, expand=1)
        img = Image.open("./assets/background.jpg")
        img = img.resize((objects.board.height*objects.board.size, objects.board.width*objects.board.size))
        self.background = ImageTk.PhotoImage(img)
        self.backgroundPic = self.canvas.create_image(0, 0, anchor=NW, image=self.background)
        self.canvas.pack(fill=BOTH, expand=1)


    def drawLine(self, x0, y0, x1, x2):
        # renders line behind player after movement
        line = self.canvas.create_line(x0, y0, x1, x2, width = 3, fill='red')
        self.root.update()
        time.sleep(.1)
        self.canvas.delete(line)

    def moveCanvas(self, xAmount, yAmount):
        # Called from player.move()
        self.canvas.move(self.playerGraphic, xAmount, yAmount)

    def moveKey(self, key, xAmount, yAmount):
        if key not in self.keys:
            return
        self.canvas.move(self.keys[key], xAmount, yAmount)

    def removeKey(self, key):
        self.canvas.delete(self.keys[key])
        del self.keys[key]

    def updateBoard(self):
        tileSize = objects.board.size
        boardHeight = objects.board.height
        boardWidth = objects.board.width
        # redraw the board
        self.canvas.delete("all")
        self.drawBackground()

        for i in range(boardWidth):
            for j in range(boardHeight):
                xpos = i * tileSize
                ypos = j * tileSize

                if objects.board.tiles[i][j].isWall():
                    rect = self.canvas.create_rectangle(xpos, ypos, xpos + tileSize, ypos + tileSize, fill='black')
                #elif objects.board.tiles[i][j].isEmpty(): 
                    #self.canvas.itemconfig(rect, fill='white')
                elif objects.board.tiles[i][j].isLava():
                    rect = self.canvas.create_rectangle(xpos, ypos, xpos + tileSize, ypos + tileSize, fill='red')
                elif objects.board.tiles[i][j].isWormhole():
                    self.canvas.pack(fill=BOTH, expand=1)
                    if objects.board.tiles[i][j].direction == "up":
                        img = Image.open("./assets/enterUp.png")
                    elif objects.board.tiles[i][j].direction == "down":
                        img = Image.open("./assets/enterDown.png")
                    elif objects.board.tiles[i][j].direction == "left":
                        img = Image.open("./assets/enterLeft.png")
                    elif objects.board.tiles[i][j].direction == "right":
                        img = Image.open("./assets/enterRight.png")
                    img = img.resize((60,60))
                    self.wormhole = ImageTk.PhotoImage(img)
                    self.canvas.create_image(   xpos + (tileSize/2),
                                                ypos + (tileSize/2),
                                                anchor=CENTER, image=self.wormhole)
                    self.canvas.pack(fill=BOTH, expand=1)
                elif objects.board.tiles[i][j].isWormholeExit():
                    rect = self.canvas.create_rectangle(xpos, ypos, xpos + tileSize, ypos + tileSize, fill='green')
                elif objects.board.tiles[i][j].isExit():
                    rect = self.canvas.create_rectangle(xpos, ypos, xpos + tileSize, ypos + tileSize, fill='gold')


    def drawPlayer(self):
        tileSize = objects.board.size
        playerSize = objects.player.size
        
        if self.playerGraphic:
            del self.playerGraphic

        #image stuff
        self.canvas.pack(fill=BOTH, expand=1)
        img = Image.open("./assets/star.jpg")
        img = img.resize((playerSize,playerSize))
        self.pic = ImageTk.PhotoImage(img)
        self.playerGraphic = self.canvas.create_image(  objects.player.x * tileSize + tileSize/2,
                                                        objects.player.y * tileSize + tileSize/2,
                                                        anchor=CENTER, image=self.pic)
        self.canvas.pack(fill=BOTH, expand=1)

        """
        self.playerGraphic = self.canvas.create_oval(objects.player.x *boardSize + (boardSize - playerSize) / 2,
													objects.player.y*boardSize + (boardSize - playerSize) / 2, 
													objects.player.x*boardSize + boardSize - (boardSize - playerSize) / 2, 
													objects.player.y*boardSize + boardSize - (boardSize - playerSize) / 2, 
													fill='red')
        """
    
    
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
        self.job = self.root.after(1000, main.main) # after() allows us to say "after 10 ms, run main()". This allows us to make a game loop inside main.py
        self.root.mainloop()

    def redrawBoard(self):
        # this function is called on by main when a game ends and the game must restart
        import main
    
        # self.root.after_cancel(self.job)    # cancels the main game loop if it's runnin
        self.updateBoard()
        self.drawPlayer()
        self.drawKeys()
        # self.job = self.root.after(500, main.main)

    # def quit(self):
    #     self.root.destroy()
    #     self.root = Tk()                     #This creates a window, but it won't show up
    #     self.root.wm_title("CSCI 166 Project       by: Joshua Holland") #Makes the title that will appear in the top left
    #     self.root.geometry("%dx%d+%d+%d" % (objects.board.width * objects.board.size, objects.board.height * objects.board.size, 130, 100))
    #     self.canvas = Canvas(self.root, width = objects.board.width * objects.board.size, height= objects.board.height * objects.board.size)
    #     self.canvas.pack()