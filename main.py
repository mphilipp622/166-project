import objects
import sys
import random
import state
import mdp
import getopt

# player, board, and graphics are instantiated in objects.py file.

def start():
	# parse arguments from command line, initialize global objects, and graphics.
	# parseArguments()
	objects.initialize()
	objects.graphics.initializeGraphics()

def restart():
	# called on by player.aiMove() function if exit condition is met
	objects.graphics.quit()
	objects.initialize()
	objects.graphics.initializeGraphics()

def moveKeys():
	for key in objects.board.keys:
		key.move(objects.board)

# def parseArguments():
# 	if len(sys.argv) > 2:
#         if "json" not in sys.argv[1]:
#             print("error: level json argument must be first argument")
#             exit()
#         if sys.argv[2] != 'v' and sys.argv[2] != 'q':
#             print("error: AI algorithm type not specified. Please use 'v' for value iteration or 'q' for q-learning")
#             exit()

# 		try:
# 			opts, args = getopt.getopt(argv,"i:",["ai=","rewardDiscount=", "livingReward=", "iterations=","learningRate="])
# 		except getopt.GetoptError:
# 			print 'main.py -i <jsonFile> ai=<v or q> rewardDiscount=<0 - 1> livingReward=<value> iterations=<value> learningRate=<value>'
# 			sys.exit(2)
# 		for opt, arg in opts:
# 			if opt == '-i':
# 				print 'test.py -i <inputfile> -o <outputfile>'
# 				sys.exit()
# 			elif opt in ("-i", "--ifile"):
# 				inputfile = arg
# 			elif opt in ("-o", "--ofile"):
# 				outputfile = arg
# 		print 'Input file is "', inputfile

# 	else:
#         print("error: not enough arguments provided. Provide level json file followed by string 'v' or 'q' for value iteration or q-learning respectively")
#         exit()

# 	return

def main():
	# Main Game Loop. Enemy movement, wormhole movement, player movement all go here

	# objects.player.move(None, random.choice(["Up", "Down", "Left", "Right"])) # Testing random player movement

	# if qlearning
	#   objects.player.aiMove(objects.qLearn.getCurrentStateActionFromPolicy(), objects.board, objects.graphics)
	objects.player.aiMove(objects.mdp.getCurrentStateActionFromPolicy(), objects.board, objects.graphics)
	moveKeys()
	objects.mdp.updateCurrentState(objects.player, objects.board.keys, None)
	objects.graphics.root.after(1000, main) # pause for 10 ms and reloop this function. SHOULD ALWAYS BE AT BOTTOM OF MAIN()

if __name__ == '__main__':
	start()