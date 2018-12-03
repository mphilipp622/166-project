import objects
import sys
import random
import state
import mdp
import getopt
import time

# player, board, and graphics are instantiated in objects.py file.

currentJob = None 	# tracks tkinter after job

def start():
	# parse arguments from command line, initialize global objects, and graphics.
	objects.initialize()
	objects.graphics.initializeGraphics()

def restart():
	# called on by player.aiMove() function if exit condition is met
	global currentJob

	if currentJob:
		objects.graphics.root.after_cancel(currentJob)
	objects.restart()
	objects.graphics.redrawBoard()

def moveKeys():
	for key in objects.board.keys:
		key.move(objects.board)

def main():
	global currentJob
	# Main Game Loop. Enemy movement, wormhole movement, player movement all go here

	if objects.valueIteration is True:
		objects.player.aiMove(objects.mdp.getCurrentStateActionFromPolicy(), objects.board, objects.graphics)
	elif objects.valueIteration is False:
		objects.player.aiQMove(objects.qLearn.getCurrentStateActionFromPolicy(), objects.board, objects.graphics)
	
	moveKeys()

	if objects.valueIteration is True:
		objects.mdp.updateCurrentState(objects.player, objects.board.keys)

	currentJob = objects.graphics.root.after(150, main) # pause for 150 ms and reloop this function. SHOULD ALWAYS BE AT BOTTOM OF MAIN()

if __name__ == '__main__':
	start()