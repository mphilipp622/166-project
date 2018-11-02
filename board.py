from tile import *

class Board:

    def __init__(self, newHeight, newWidth, newSize):
        self.height = newHeight
        self.width = newWidth
        self.size = newSize
        self.makeBoard(None)

    def makeBoard(self, filename):
        # this function needs to be updated to handle reading a level from saved file

        self.tiles = [[Tile("empty") for x in range(self.width)] for y in range(self.height)]
        self.tiles[0][10].type = "wall"
        self.tiles[5][5].type = "wall"
        self.tiles[4][14].type = "wall"