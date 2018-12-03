# Skate Space

This project was created for Fresno State's CSCI 166 - Principles of Artificial Intelligence class, taught by professor David Ruby.

In this project, we explore value iteration and Q-learning inside a grid-world. The distinguishing feature of this world versus most grid worlds is that movement in a direction does not stop until the agent runs into an obstacle.

The goal of the agent is to collect the keys that are in the level and go to the exit. Doing so will win the level. The catch is that the keys can also move, so the agent must make informed decisions about when to wait and move in order to get a key.

## Developers

[Zachary Andersen](https://github.com/Xakaree)
Abhishek Gupta
[Joshua Holland](https://github.com/ggkfox)
Juan Mejia
[Mark Philipp](https://github.com/mphilipp622)

## Pre-requisites

The project can be run using Python 2.7 or Python 3+

The following modules must be installed to compile and run the program:

	- TKinter
	- pillow
	- keyboard
	
It's recommended to use pip to install the above packages. E.G:
**pip install pillow**
**pip install keyboard**
**pip install tkinter.**

NOTE: Python 2 uses a capital T for Tkinter. Python 3 is all lowercase: tkinter

## How to run

Open a python terminal and navigate to the root directory of the repository. Once inside, run the following syntax:

python main.py <nameOfJsonFile>.json <v or q>

where <nameOfJsonFile> is the name of the level you wish to load. <v or q> means that you can put either v or q in this spot to run value iteration or q-learning. Value iteration uses the 'v' parameter and q-learning uses the 'q' parameter.

Here's an example compilation:

**python main.py testValueIter.json v**

This will run the testValueIter level using value iteration.

Another example:

**python main.py testValueIter2.json q**

This will run the testValueIter2 level using q learning.

## Value Iteration Compilation Time

Value iteration takes a relatively long time to compute, especially for large levels. You might have to be patient while waiting for the program to start running.

## Modifying the AI Variables

For value iteration, you can modify the number of iterations, the reward discount, and the living reward in the **mdp.py** file in the MDP class constructor.

For Q-Learning, you can modify Epsilon, reward discount, living reward, and learning rate by going to the **qLearning.py** file and changing the values in the QLearn class constructor.
