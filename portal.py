import portalExit
import tile

# Portal inherits from Tile
class Portal(tile.Tile):

    def __init__(self, entranceDirection, newExit):
        self.direction = entranceDirection
        self.exit = newExit
        self.type = "wormhole"

    def getPortalExit(self):
        return self.exit