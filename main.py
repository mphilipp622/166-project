import objects
import sys
import random

# player, board, and graphics are instantiated in objects.py file.

def start():
    # initialize tkinter graphics
    objects.graphics.initializeGraphics()

def moveKeys():
    for key in objects.board.keys:
        key.move(objects.board)

def main():

    # Main Game Loop. Enemy movement, wormhole movement, player movement all go here

    # objects.player.move(None, random.choice(["Up", "Down", "Left", "Right"])) # Testing random player movement

    moveKeys()
    # objects.graphics.drawKeys()
    objects.graphics.root.after(1000, main) # pause for 10 ms and reloop this function. SHOULD ALWAYS BE AT BOTTOM OF MAIN()

if __name__ == '__main__':
    start()