import tile

class PortalExit(tile.Tile):

    def __init__(self, newDirection):
        self.direction = newDirection
        self.type = "wormholeExit"
        self.key = False