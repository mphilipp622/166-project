import tile

class PortalExit(tile.Tile):

    def __init__(self, x, y, newDirection):
        self.direction = newDirection
        self.type = "wormholeExit"
        self.key = False
        self.exitX = x
        self.exitY = y
