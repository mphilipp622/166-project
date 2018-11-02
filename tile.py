import enum
import portalExit

# this enum is used for tracking the type of this tile. Instead of using 4 booleans, we can check against this enum.
# this is useful for consolidating the constructor
class TileType(enum.Enum):
    empty = 0
    wall = 1
    lava = 2
    portal = 3

class Tile:
    
    def __init__(self, tileType, portalExit = None):    
        # portalExit defaults to nothing unless specified during instantiation.
        self.type = tileType
        self.portalExit = portalExit

    def isWall(self):
        return self.type == TileType.wall

    def isLava(self):
        return self.type == TileType.lava

    def isPortal(self):
        return self.type == TileType.portal

    def isEmpty(self):
        return self.type == TileType.empty
