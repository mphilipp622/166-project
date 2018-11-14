
class State:

    def __init__(self, player, wormholes, keys):
        self.playerPos = (player.x, player.y)
        # self.wormholes = [(wormhole.x, wormhole.y) for wormhole in wormholes]
        self.keys = [(key.x, key.y) for key in keys]

    # overload this class's equality operator so it checks if all the positions are the same.
    # Returns true if all positions are the same, regardless of which order they are stored in the lists
    def __eq__(self, other):
        return 
        (
                self.playerPos == other.playerPos 
                and ( set(self.keys) == set(other.keys) )
                and ( set(self.wormholes) == set(other.wormholes) )
        )