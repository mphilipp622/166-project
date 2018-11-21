import objects
import itertools
import state

class QLearn:

	def __init__(self, startingState, rewardDiscount = 0.5, livingReward = -1, learningRate = 0.2, epsilon = 0.25):
		self.currentState = startingState
		self.states = list()                # contains all the valid states of the model
		# self.policyTable = dict()           # this will be a dictionary of ((State, action) : action) pairs.
		# self.currentStateValues = dict()    # dictionary of ((State, action) : value) pairs. Used for storing Q(s, a)
		# self.nextStates = dict()            # dictionary of (state, action) keys that returns the State that (s,a) will go to.
		self.rewardDiscount = rewardDiscount
		self.livingReward = livingReward
		self.learningRate = learningRate
		self.epsilon = epsilon
  
		self.qTable = dict()    # will store q values using (state, action) keys and a floating point value

		self.initializeStates()                         # initialize all the states that exist in the MDP
		# self.initializeNextStateTable()   # initialize table of next states given original state and R(s,a,s') for all states and actions

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
			
			for action in self.getActionVector(stateObj, objects.board):
				self.qTable[(stateObj, action)] = 0   # initialize state's value to 0 in the dictionary

		self.qTable[(None, None)] = 0   # this will be used for the exit state

		# for key, val in self.currentStateValues.items():
		#     print key
		#     print val

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

	def initializeNextStateTable():
		return

	def updateState(self, rewardReceived):
		# Q_k+1(s, a) = (1 - learningRate)(Q_k(s, a)) + learningRate(R(s, a, s') + rewardDiscount(max_a'(Q_k(s', a'))))
		newState = state.State((objects.player.x, objects.player.y), [(key.x, key.y) for key in objects.board.keys], None)

		self.currentState = newState
		return

	def getCurrentStateActionFromPolicy(self):
		return

	# def updateCurrentState(self, player, keys, wormholes):
	# 	keyVector = list()
		
	# 	for key in keys:
	# 		# check if the key has been acquired. If it has, we want to append None so the state can keep track properly
	# 		if key.acquired:
	# 			keyVector.append(None)
	# 		else:
	# 			keyVector.append((key.x, key.y))

	# 	newState = state.State((player.x, player.y), keyVector, wormholes)
	# 	self.currentState = newState