import board
from player import Player
import sys
import random

#--------GLOBAL VARIABLES--------
h = 10          #number of tiles vertically
w = 15          #number of tiles horrizontally
size = 60       #size of tiles
delay = .02   #smaller the number the faster the player moves
global myPlayer
myPlayer = Player(0, 0, arr)

global myBoard

#2D array of objects that are the tiles
arr = [[0 for x in range(w)] for y in range(h)]
arr[0][10] = 1
arr[5][5] = 1
arr[4][14] = 1

def updateBoard():
    canvas.delete("all")
    for i in range(h):
        for j in range(w):
            xpos = j*size
            ypos = i*size
            rect = canvas.create_rectangle(xpos, ypos, xpos+size, ypos+size, fill='#FFF')
            if arr[i][j]==1:
                canvas.itemconfig(rect, fill='black')
            else: 
                canvas.itemconfig(rect, fill='white')


#-------CODE!!!----------
updateBoard()



