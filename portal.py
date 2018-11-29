import portalExit
import tile

# Portal inherits from Tile
class Portal(tile.Tile):

    def __init__(self, entranceDirection, newExit):
        self.direction = entranceDirection
        self.exit = newExit
        self.type = "wormhole"
        self.key = False
        self.portalMechanics = {}
        self.portalMechanics["up"] = {
            "Up" : "Up", "Right" : "Right", "Down" : "Down", "Left" : "Left"
        }
        self.portalMechanics["down"] = {
            "Up" : "Down", "Right" : "Left" , "Down" : "Up", "Left" : "Right"
        }
        self.portalMechanics["left"] = {
            "Up" : "Right", "Right" : "Down", "Down" : "Left", "Left" : "Up"
        }
        self.portalMechanics["right"] = {
            "Up" : "Left", "Right" : "Up", "Down" : "Right", "Left" : "Down"
        }

    def getPortalExit(self):
        return self.exit

    def translateDirection(self, action, thePlayer):
        eDirection = portalMechanics[self.direction][action]
        newAction = portalMechanics[self.exit.direction][eDirection]
        thePlayer.overrideAction = newAction
