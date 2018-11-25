
class State:

    def __init__(self, playerPos, keyPos, wormholePos):
        self.playerPos = playerPos
        # self.wormholes = [wormhole for wormhole in wormholePos]
        self.keyPositions = keyPos
        # self.currentValue = 0   # used for value iteration. Values are always initialized to 0 at time 0

    def __eq__(self, other):
        # overload this class's equality operator so it checks if all the positions are the same.
        # Returns true if all positions are the same, regardless of which order they are stored in the lists
        return(
                self.playerPos == other.playerPos 
                and ( self.keyPositions == other.keyPositions )
        )
                # and ( set(self.wormholes) == set(other.wormholes) ))

    def __hash__(self):
        # return hash((self.playerPos, self.keyPositions, self.wormholes))
        return hash((str(self.playerPos), str(self.keyPositions)))

    def __repr__(self):
        return "[ p" + str(self.playerPos) + ", K(" + str(self.keyPositions) + ")]"

    def __str__(self):
        # overloads the print operator for this class so it prints the returned string below
        return "[ p" + str(self.playerPos) + ", K(" + str(self.keyPositions) + ")]"