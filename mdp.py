import state
import objects
import itertools
import board
import copy
import time

class MDP:

    def __init__ (self, startingState, iterations = None):
        self.currentState = startingState
        self.states = list()                # contains all the valid states of the model
        self.policyTable = dict()           # this will be a dictionary of (state : action) pairs. This will be updated by value iteration and q-learning
        self.currentStateValues = dict()    # dictionary of (State : float) pairs. Used for value iteration. This will hold V_K values
        self.nextStates = dict()            # dictionary of (state, action) keys that returns the State that (s,a) will go to.
        self.transitionFunctions = dict()   # will contain (s,a) tuple for the key and returns a list of (action, probability) tuples
        self.rewardFunctions = dict()       # will contain (s,a,s') tuple for the key and a reward value   
        self.rewardDiscount = 0.5
        self.livingReward = -1
        self.intendedActionProbability = 0.8    # intended action succeeds 80% of the time
        self.unintendedActionProbability = 0.2  # unintended action occurs 20% of the time. This will be split by the number of unintended actions available in a state
        self.iterations = iterations if iterations != None else 10

        self.initializeStates()                         # initialize all the states that exist in the MDP
        self.initializeNextStateTableAndRewardTable()   # initialize table of next states given original state and R(s,a,s') for all states and actions
        self.initializeTransitionFunctions()            # initialize T(s,a,s') for all states and actions
        
        start = time.time()
        self.valueIteration()
        end = time.time()
        print (end - start)
        # for key, val in self.currentStateValues.items():
        #     print key
        #     print val

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
            self.currentStateValues[stateObj] = 0   # initialize state's value to 0 in the dictionary

        self.currentStateValues[None] = 0   # this will be used for the exit state

        # for key, val in self.currentStateValues.items():
        #     print key
        #     print val

    def initializeNextStateTableAndRewardTable(self):
        for currentState in self.states:
            # iterate over all states
            for action in self.getActionVector(currentState, objects.board):
                nextState, reward = self.getNextStateAndReward(currentState, action)
                self.nextStates[(currentState, action)] = nextState
                self.rewardFunctions[(currentState, action, nextState)] = reward

    def initializeTransitionFunctions(self):

        # iterate over all the states
        for newState in self.states:
            actionVector = self.getActionVector(newState, objects.board)

            if len(actionVector) == 1:
                transitionProbabilityList = [(actionVector[0], 0.8)]
                self.transitionFunctions[(newState, actionVector[0])] = transitionProbabilityList
            else:
                # set the main action to 80% probability and the rest to 20% / size of the remaining possible actions.
                for action in actionVector:   
                    mainAction = (action, self.intendedActionProbability)

                    remainingProbability = self.unintendedActionProbability / (len(actionVector) - 1)    # calculates probability for any action that isn't the main action
                    transitionProbabilityList = [mainAction]
                    
                    for newAction in actionVector:
                        if newAction == action:
                            continue
                
                    transitionProbabilityList.append((newAction, remainingProbability))
            
                    self.transitionFunctions[(newState, action)] = transitionProbabilityList

    def getActionVector(self, currentState, board):
        # helper function called by valueIteration() to get a vector of valid directions from the position passed.
        # NOTE: playerPos is a tuple of (x, y) type. So playerPos[0] gives x value and playerPos[1] gives y value
        x = currentState.playerPos[0]
        y = currentState.playerPos[1]

        validMoves = ["Left", "Right", "Up", "Down", "Stay"]

        if board.tiles[x][y].isExit() and all(val == None for val in currentState.keyPositions):
            validMoves = ["Exit"]   # player is on exit and has all the keys, exit is the only right move.
            return validMoves

		# rule out which actions we can take depending on current and next x, y positions. Based on implementation in key.py
        if x == 0 or board.tiles[x - 1][y].isWall():
            validMoves.remove("Left")
        if x == board.width - 1 or board.tiles[x + 1][y].isWall():
        	validMoves.remove("Right")
        if y == 0 or board.tiles[x][y - 1].isWall():
        	validMoves.remove("Up")
        if y == board.height - 1 or board.tiles[x][y + 1].isWall():
            validMoves.remove("Down")

        return validMoves
    
    def getNextStateAndReward(self, originalState, action):
        # calculates next state and reward value based on action taken in originalState
        # value is returned as a tuple (nextState, rewardValue)

        # these bools track if player died or got a key taking this action

        if action == "Exit":
            # if we can exit, return 100 reward
            return (None, 100)
        if action == "Stay":
            # if we stay, return the state we were just in
            return (originalState, 0)

        totalReward = 0 # track the reward we end up getting for taking this action
        xDirection = 0
        yDirection = 0

        # create temporary movement variables so player isn't actually effected
        playerX = originalState.playerPos[0]
        playerY = originalState.playerPos[1]
        tempBoard = copy.deepcopy(objects.board) # create a copy of the board
        nextState = None
        resultingKeyPositionList = copy.deepcopy(originalState.keyPositions) # this list will be updated if keys are acquired taking this action

        # assign keys to the board
        for key in tempBoard.keys:
            tempBoard.tiles[key.x][key.y].key = False
        for keyPos in originalState.keyPositions:
            if keyPos is None:
                continue
            tempBoard.tiles[keyPos[0]][keyPos[1]].key = True

        # assign wormholes to the board
        # for wormhole in tempBoard.wormholes:
        #     wormhole.type = "empty"
        # for wormholePos in originalState.wormholes:
        #     tempBoard.tiles[wormholePos[0]][wormholePos[1]].type = "wormhole"

        tempKeyCount = 0

        for key in originalState.keyPositions:
            if key == None:
                tempKeyCount += 1 # if a key is set to None in the key vector, add to the key count

        # note that the x, y origin is at the top-left, which is why UP is -1 in the y direction.
        if action == "Down":
            yDirection = 1
        elif action == "Up":
            yDirection = -1
        elif action == "Right":
            xDirection = 1
        elif action == "Left":
            xDirection = -1

        if yDirection != 0:
            while ((playerY + yDirection >= 0 and playerY + yDirection < tempBoard.height) and 
            not (tempBoard.tiles[playerX][playerY + yDirection].isWall())):
                playerY += yDirection

                if tempBoard.tiles[playerX][playerY].hasKey():
                    totalReward += 10

                    # iterate over key position list and set the key that was acquired to None
                    for index, keyPos in enumerate(resultingKeyPositionList):
                        if keyPos is None:
                            continue

                        if keyPos[0] == playerX and keyPos[1] == playerY:
                            resultingKeyPositionList[index] = None

                if tempBoard.tiles[playerX][playerY].isLava():
                    totalReward -= 1000
            
        elif xDirection != 0:
            while ((playerX + xDirection >= 0 and playerX + xDirection < tempBoard.width) and 
            not (tempBoard.tiles[playerX + xDirection][playerY].isWall())):
                playerX += xDirection

                if tempBoard.tiles[playerX][playerY].hasKey():
                    totalReward += 10

                    # iterate over key position list and set the key that was acquired to None
                    for index, keyPos in enumerate(resultingKeyPositionList):
                        if keyPos is None:
                            continue

                        if keyPos[0] == playerX and keyPos[1] == playerY:
                            resultingKeyPositionList[index] = None

                if tempBoard.tiles[playerX][playerY].isLava():
                    totalReward -= 1000

        nextState = state.State((playerX, playerY), resultingKeyPositionList, None)
        # self.rewardFunctions[(originalState, action, nextState)] = totalReward
        return (nextState, totalReward)
        
    def valueIteration(self):
        # perform value iteration
        # iterate 100 times over all states and update values
        for i in range(0, self.iterations):
            # grab our kth dictionary of values
            previousStateValues = copy.deepcopy(self.currentStateValues)

            for currentState in self.states:
                actionVector = self.getActionVector(currentState, objects.board)
                actionValues = dict()   # will track (action : value) key-value pairs. Will take argmax after getting all values
                
                # iterate over each action and append values to actionValues dictionary
                for action in actionVector:
                    # calculate T(s, a, s') * (R(s, a, s') + rewardDiscount(V_K(s')))
                    actionValues[action] = 0

                    # T(s,a,s') returns 0.8 for intented action and the remaining actions that are possible take up the remaining 20% combined.
                    for newAction, probability in self.transitionFunctions[(currentState, action)]:
                        # if intended action is right, right will succeed at 0.8, up, down, left, and stay will succeed with 0.05
                        nextState = self.nextStates[(currentState, newAction)]
                        reward = self.rewardFunctions[(currentState, newAction, nextState)]
                        actionValues[action] += probability * (reward + (self.rewardDiscount * previousStateValues[nextState]))

                self.currentStateValues[currentState] = max(actionValues.values()) # Update state value to new values that were just calculated.
                self.policyTable[currentState] = max(actionValues, key=actionValues.get) # update policy of currentState to the best action from the calculation

    def getKeyPositionCombinations(self):
        # get key positions for each key. We have min and max x,y positions for each key that must be considered
        counter = 0
        keyPos = [list() for x in range(0, len(objects.board.keys))]

        for key in objects.board.keys:
            for x in range(key.xmin, key.xmax + 1):
                for y in range(key.ymin, key.ymax + 1):
                    if objects.board.tiles[x][y].isWall():
                        # wall tiles are not valid key positions
                        continue

                    keyPos[counter].append((x, y)) # add a position for this specific key.
            
            keyPos[counter].append(None)
            counter += 1

        # get cartesian product of all key positions. This gives us all possible key position combinations
        keyCombos = list(set(itertools.product(*keyPos)))

        # Find entries that contain duplicate positions. Keys cannot be on top of one another.
        removeList = list()
        for i in range(0, len(keyCombos)):
            for j in range(0, len(objects.board.keys)):
                for k in range(0, len(objects.board.keys)):
                    if j == k:
                        continue
                    if keyCombos[i][j] == keyCombos[i][k] and (keyCombos[i][j] and keyCombos[i][k] != None):
                        removeList.append(keyCombos[i])
                        break

        return [list(positions) for positions in keyCombos if positions not in removeList]
        # print keyList

    def getWormholePositionCombinations(self):
        # get possible positions for each wormhole.
        counter = 0
        wormholePositions = [list() for x in range(0, len(objects.board.wormholes))]

        for wormhole in objects.board.wormholes:
            for x in range(0, len(objects.board.tiles)):
                for y in range(0, len(objects.board.tiles[0])):
                    if objects.board.tiles[x][y].isWall():
                        # wall tiles are not valid key positions
                        continue

                    wormholePositions[counter].append((x, y)) # add a position for this specific key.
            
            counter += 1

        # get cartesian product of all key positions. This gives us all possible key position combinations
        wormholeCombos = list(set(itertools.product(*wormholePositions)))

        # Find entries that contain duplicate positions. Keys cannot be on top of one another.
        removeList = list()
        for i in range(0, len(wormholeCombos)):
            for j in range(0, len(objects.board.wormholes)):
                for k in range(0, len(objects.board.wormholes)):
                    if j == k:
                        continue
                    if wormholeCombos[i][j] == wormholeCombos[i][k]:
                        removeList.append(wormholeCombos[i])
                        break

        return [positions for positions in wormholeCombos if positions not in removeList]

    def updateCurrentState(self, player, keys, wormholes):
        keyVector = list()
        for key in keys:
            # check if the key has been acquired. If it has, we want to append None so the state can keep track properly
            if key.acquired:
                keyVector.append(None)
            else:
                keyVector.append((key.x, key.y))

        newState = state.State((player.x, player.y), keyVector, wormholes)
        self.currentState = newState

    def getCurrentStateActionFromPolicy(self):
        # returns the best action for the current state of the MDP
        # print str(self.currentState) + " = " + str(self.currentStateValues[self.currentState])
        return self.policyTable[self.currentState]