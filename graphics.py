import keyboard
from tkinter import *
import time

def drawLine(x0, y0, x1, y1):
    line = self.canvas.create_line(x0, y0, x1, x2, width = 3, fill='red')
    root.update()
    time.sleep(.2)
    self.canvas.delete(line)

#-------Tkinter stuff--------
root = Tk()                     #This creates a window, but it won't show up
root.wm_title("CSCI 166 Project       by: Joshua Holland") #Makes the title that will appear in the top left
root.geometry("%dx%d+%d+%d" % (w*size, h*size, 130, 100))
canvas = Canvas(root, width=w*size, height=h*size, background='black')


root.bind("<Up>", lambda event: myPlayer.move(event, newDirection = "Up"))
root.bind("<Down>", lambda event: myPlayer.move(event, newDirection = "Down"))
root.bind("<Left>", lambda event: myPlayer.move(event, newDirection = "Left"))
root.bind("<Right>", lambda event: myPlayer.move(event, newDirection = "Right"))
canvas.pack()

p = canvas.create_oval(0+(size - myPlayer.size)/2, 0+(size - myPlayer.size)/2, 0+size-(size - myPlayer.size)/2, 0+size-(size - myPlayer.size)/2, fill='red')

#----must be at end----
root.mainloop()