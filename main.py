import objects
import sys
import random
import state
import mdp
import getopt

# player, board, and graphics are instantiated in objects.py file.

def start():
	# parse arguments from command line, initialize global objects, and graphics.
	objects.initialize()
	objects.graphics.initializeGraphics()

def restart():
	# called on by player.aiMove() function if exit condition is met
	objects.graphics.quit()
	objects.restart()
	objects.graphics.initializeGraphics()

def moveKeys():
	for key in objects.board.keys:
		key.move(objects.board)

def main():
	# Main Game Loop. Enemy movement, wormhole movement, player movement all go here

	# objects.player.move(None, random.choice(["Up", "Down", "Left", "Right"])) # Testing random player movement

	# if qlearning
	#   objects.player.aiMove(objects.qLearn.getCurrentStateActionFromPolicy(), objects.board, objects.graphics)
	if objects.valueIteration is True:
		objects.player.aiMove(objects.mdp.getCurrentStateActionFromPolicy(), objects.board, objects.graphics)
	elif objects.valueIteration is False:
		objects.player.aiMove(objects.qLearn.getCurrentStateActionFromPolicy(), objects.board, objects.graphics)
	
	moveKeys()
	objects.mdp.updateCurrentState(objects.player, objects.board.keys, None)
	objects.graphics.root.after(1000, main) # pause for 10 ms and reloop this function. SHOULD ALWAYS BE AT BOTTOM OF MAIN()

if __name__ == '__main__':
	start()