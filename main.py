import board
import player
import sys
import keyboard
from Tkinter import *
import time
import random

#--------GLOBAL VARIABLES--------
h = 10          #number of tiles vertically
w = 15          #number of tiles horrizontally
size = 60       #size of tiles
delay = .02   #smaller the number the faster the player moves

#2D array of objects that are the tiles
arr = [[0 for x in range(w)] for y in range(h)]
arr[0][10] = 1
arr[5][5] = 1
arr[4][14] = 1

def moveUp(event):
    if (player.y-1 < 0): return
    if (arr[player.y-1][player.x] == 1): return
    else:
        player.y -= 1
        canvas.move(p, 0, -size)
        time.sleep(delay)
        moveUp(event)

def moveDown(event):
    if (player.y+2 > h): return
    if (arr[player.y+1][player.x] == 1): return
    else:
        player.y += 1
        canvas.move(p, 0, size)
        root.update()
        time.sleep(delay)
        moveDown(event)

def moveLeft(event):
    if (player.x-1 < 0): return
    if (arr[player.y][player.x-1] == 1): return
    else:
        player.x -= 1
        canvas.move(p, -size, 0)
        root.update()
        time.sleep(delay)
        moveLeft(event)

def moveRight(event):
    if (player.x+2 > w): return
    if (arr[player.y][player.x+1] == 1): return
    else:
        player.x += 1
        canvas.move(p, size, 0)
        root.update()
        time.sleep(delay)
        moveRight(event)

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
            # if (i==player.y and j==player.x): 
                # p = canvas.create_oval(xpos+(size-player.size)/2, ypos+(size-player.size)/2, xpos+size-(size-player.size)/2, ypos+size-(size-player.size)/2, fill='blue')

#-------Tkinter stuff--------
root = Tk()                     #This creates a window, but it won't show up
root.wm_title("CSCI 166 Project       by: Joshua Holland") #Makes the title that will appear in the top left
root.geometry("%dx%d+%d+%d" % (w*size, h*size, 130, 100))
canvas = Canvas(root, width=w*size, height=h*size, background='black')
root.bind("<Up>", moveUp)
root.bind("<Down>", moveDown)
root.bind("<Left>", moveLeft)
root.bind("<Right>", moveRight)
canvas.pack()

#-------CODE!!!----------
updateBoard()
p = canvas.create_oval(0+(size-player.size)/2, 0+(size-player.size)/2, 0+size-(size-player.size)/2, 0+size-(size-player.size)/2, fill='red')

#----must be at end----
root.mainloop()