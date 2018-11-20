import tile

class PortalExit(tile.Tile):

    def __init__(self, newDirection, exitX, exitY):
        self.direction = newDirection
        self.type = "wormholeExit"
        self.key = False
        self.exitX = exitX
        self.exitY = exitY
