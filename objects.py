import player as playerLibrary
import board as boardLibrary
import graphics as graphicsLibrary
import sys
import state
import mdp as mdpLibrary
import qLearning as qLearningLibrary
import stateHandler

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

		if sys.argv[2] == 'v':
			valueIteration = True
		else:
			valueIteration = False

		# boardConstructor(height, width, tileSize)
		board = boardLibrary.Board(sys.argv[1])

		#playerConstructor(startingXPos, startingYPos)
		player = playerLibrary.Player(board.playerPosition[0], board.playerPosition[1])

		startingState = state.State((player.x, player.y), [(key.x, key.y) for key in board.keys], None)
		# if stateHandler is None:
		# 	stateHandler = stateHandler.StateHandler(state.State((player.x, player.y), [(key.x, key.y) for key in board.keys], None))
		if valueIteration is True:
			mdp = mdpLibrary.MDP(startingState)
			qLearn = None
		else:
			qLearn = qLearningLibrary.QLearn(startingState)
			mdp = None

		# currentState = state.State(player, None, board.keys)    # tracks the current state of the game.

		graphics = graphicsLibrary.Graphics()

		# if sys.argv[2] == 'v':
		#     ai = mdpLibrary.MDP(state.State((player.x, player.y), [(key.x, key.y) for key in board.keys], None))
		# elif sys.argv[2] == 'q':
		#     ai = qLearningLibrary.QLearn(state.State((player.x, player.y), [(key.x, key.y) for key in board.keys], None))
	else:
		print("error: not enough arguments provided. Provide level json file followed by string 'v' or 'q' for value iteration or q-learning respectively")
		exit()

def restart():
	global board, player, graphics, mdp, valueIteration, qLearn, stateHandler
	# boardConstructor(height, width, tileSize)
	board = boardLibrary.Board(sys.argv[1])

	#playerConstructor(startingXPos, startingYPos)
	player = playerLibrary.Player(board.playerPosition[0], board.playerPosition[1])

	# if we run restart, we already know we have an mdp or a qlearn object.
	if valueIteration is True:
		mdp.currentState = state.State((player.x, player.y), [(key.x, key.y) for key in board.keys], None)
	else:
		qLearn.iterations += 1.0
		qLearn.currentState = state.State((player.x, player.y), [(key.x, key.y) for key in board.keys], None)
		print("Iterations: " + str(qLearn.iterations))
		print("Win Rate = " + str(round(qLearn.getWinRate(), 2)) + "%")
	# graphics = graphicsLibrary.Graphics()