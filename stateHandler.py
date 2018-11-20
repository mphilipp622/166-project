import state
import objects

class StateHandler:

    def __init__(self, startingState):
        self.states = List()
        self.currentState = startingState

        self.initializeStates()

    def initializeStates(self):
        # iterates over the board and creates every valid state that exists in the MDP.
        # this is gonna be computationally expensive as shit.

        # get all possible player, key, and wormhole positions. Positions are stored as a tuple of (x, y) coordinates.
        # Note that these are ALL positions each of these items can occupy.
        playerPos = list()
        # wormholePos = list()
        keyPos = list()

        # get player positions
        for x in range(0, len(objects.board.tiles)):
            for y in range(0, len(objects.board.tiles[0])):

                if objects.board.tiles[x][y].isWall():
                    continue
                
                # if this tile is avalid player position, add it to list.
                playerPos.append((x, y))   
        
        # get all valid combinations of key positions.
        keyList = self.getKeyPositionCombinations()
        
        # get all valid wormhole combinations of positions
        # wormholeList = self.getWormholePositionCombinations()
        # stateList = list(itertools.product(playerPos, keyList, wormholeList))
        
        # populate list of all possible states
        stateList = list(itertools.product(playerPos, keyList))
        
        for newState in stateList:
            stateObj = state.State(newState[0], newState[1], None)
            self.states.append(stateObj) # will change to state.State(state[0], state[1], state[2]) once wormholes are in.

        # for key, val in self.currentStateValues.items():
        #     print key
        #     print val