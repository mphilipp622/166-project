import player as playerLibrary
import board as boardLibrary
import graphics as graphicsLibrary
import sys
import state
import mdp as mdpLibrary
import qLearning as qLearningLibrary

# This file is used by main, player, and board for accessing instances of these classes for cross communication

board = None
player = None
graphics = None
mdp = None
valueIteration = None
qLearn = False
stateHandler = False

def initialize():
	global board, player, graphics, mdp, valueIteration, qLearn, stateHandler

	if len(sys.argv) > 2:
		if "json" not in sys.argv[1]:
			print("error: level json argument must be first argument")
			exit()
		if sys.argv[2] != 'v' and sys.argv[2] != 'q':
			print("error: AI algorithm type not specified. Please use 'v' for value iteration or 'q' for q-learning")
			exit()

		rewardArgument = None
		livingReward = None
		iterations = None
		learninRate = None
		epsilon = None

		if sys.argv[2] == 'v':
			if len(sys.argv) != 6:
				print("Error: value iteration requires reward discount, living reward, and number of iterations.\npython main.py level.json v 0.8 -1 50")
				exit()
			valueIteration = True
			iterations = int(sys.argv[5])
		else:
			if len(sys.argv) != 7:
				print("Error: q learning requires reward, living reward, learning rate, and epsilon.\npython main.py level.json 0.8 -1 0.2 0.9")
				exit()
			valueIteration = False
			learningRate = float(sys.argv[5])
			epsilon = float(sys.argv[6])

		rewardArgument = float(sys.argv[3])
		livingReward = float(sys.argv[4])
		board = boardLibrary.Board(sys.argv[1])

		player = playerLibrary.Player(board.playerPosition[0], board.playerPosition[1])

		startingState = state.State((player.x, player.y), [(key.x, key.y) for key in board.keys])

		if valueIteration is True:
			mdp = mdpLibrary.MDP(startingState, rewardArgument, livingReward, iterations)
			qLearn = None
		else:
			qLearn = qLearningLibrary.QLearn(startingState, rewardArgument, livingReward, learningRate, epsilon)
			mdp = None

		graphics = graphicsLibrary.Graphics()

	else:
		print("error: not enough arguments provided. Provide level json file followed by string 'v' or 'q' for value iteration or q-learning respectively")
		exit()

def restart():
	global board, player, graphics, mdp, valueIteration, qLearn, stateHandler

	board = boardLibrary.Board(sys.argv[1])

	player = playerLibrary.Player(board.playerPosition[0], board.playerPosition[1])

	# if we run restart, we already know we have an mdp or a qlearn object.
	if valueIteration is True:
		mdp.currentState = state.State((player.x, player.y), [(key.x, key.y) for key in board.keys])
	else:
		qLearn.iterations += 1.0
		qLearn.currentState = state.State((player.x, player.y), [(key.x, key.y) for key in board.keys])
		print("Iterations: " + str(qLearn.iterations))
		print("Win Rate = " + str(round(qLearn.getWinRate(), 2)) + "%")