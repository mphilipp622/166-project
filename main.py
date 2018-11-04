import objects
import sys
import random

# player, board, and graphics are instantiated in objects.py file.

def start():
    objects.graphics.initializeGraphics()

def main():

    # Main Game Loop. Enemy movement, wormhole movement, player movement all go here

    # objects.player.move(None, random.choice(["Up", "Down", "Left", "Right"])) # Testing random player movement


    objects.graphics.root.after(10, main) # pause for 10 ms and reloop this function. SHOULD ALWAYS BE AT BOTTOM OF MAIN()

if __name__ == '__main__':
    start()