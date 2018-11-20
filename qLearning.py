
class QLearn:

	def __init__(self, rewardDiscount = 0.5, livingReward = -1, learningRate = 0.2, epsilon = 0.25):
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
		self.initializeNextStateTable()   # initialize table of next states given original state and R(s,a,s') for all states and actions

	def initializeStates(self):
		return

	def initializeNextStateTable():
		return

	def updateState(self, rewardReceived):
		# Q_k+1(s, a) = (1 - learningRate)(Q_k(s, a)) + learningRate(R(s, a, s') + rewardDiscount(max_a'(Q_k(s', a'))))
		return

	def getCurrentStateActionFromPolicy(self):
		return