import portalExit
import tile

# Portal inherits from Tile
class Portal(tile.Tile):

    def __init__(self, entranceDirection, newExit):
        self.direction = entranceDirection
        self.exit = newExit
        self.type = "wormhole"
        self.key = False

    def getPortalExit(self):
        return self.exit