from random import randrange
from time import time
from copy import deepcopy

# board output
def printBoard(board):
	print("---------------------------")
	for row in range(9):
		print(" ".join(map(str,board[row]))) # clear the commas and the brackets
	print("---------------------------")

# board generation functions
def clearRow(row,board):
	for col in range(9):
		board[row][col]=0 # clear the specified row

def checkValid(number,row,col,board):
	'''this function checks the validity of a given number by iterating over the the board in a 'T' like pattern '''
	for ro in range(9):  # loop over all rows 
		if ro ==row: # check if the current is row the row of the provided number
			for num in board[ro]: # loop through each number in the row
				if num == number: # check if there is a number equal to the provided number in the row
					return 1
		if board[ro][col] ==number: # check if the number is equal to the provided number in the provided column
			return 1
	return 0

def fillCol(row,board):
	for col in range(9): # loop over the columns 
		num = randrange(1,10) # generate random number
		forbid=[] # this list is used to prevent using an invalid number more than once
		while checkValid(num,row,col,board):
			forbid.append(num) # add the number to the list of forbidden numbers
			num=randrange(1,10)
			while num in forbid: # keep generating random numbers until the number is not forbidden 
				if len(forbid)==9: # if all 9 numbers are invalid (the whole row must be cleared and the process must start over)
					return 0
				num=randrange(1,10) # generate another number
		board[row][col]=num # finally, if the number is valid, add it to the board
	return 1

def rowGenerator(board):
	start = time()
	for row in range(9):
		while not fillCol(row,board): # keep clearing the rows until a combination is valid (There are 362,880 possible combinations in a single row)
			clearRow(row,board)
	duration=time()-start
	return duration

# question board generation function
def troubleMaker(board,difficulty):
	'''this function is used to create the question board by clearing random places in the board'''
	troubledBoard = deepcopy(board) # make a deep copy of the original board so that it does not get overwritten.
	for row in range(9):
		emptyPlaces = randrange(difficulty,difficulty+4) # generate a random number of empty places for each row
		emptyCols=[] # this list is used so that a previously empty place does not change again instead of another one
		while emptyPlaces>0:
			col=randrange(0,9) # generate a random col (random number for the empty place ie. its position)
			while col in emptyCols:
				col =randrange(0,9)
			emptyCols.append(col)
			troubledBoard[row][col]=' ' # clear the place
			emptyPlaces -= 1 # reduce the number of empty places in the row (to be cleared)
	return troubledBoard

# user input handling function
def inputHandler(text,options):
	'''this function is used to prompt the user to answer different questions'''
	valid = 0
	while not valid:
		try:
			userChoice = int(input(text))
		except ValueError:
			print("invalid")
			continue
		else:
			if userChoice in options:
				break
			else:
				print("invalid")
	return userChoice

# no brainer
def main():
	board=[[0,0,0,0,0,0,0,0,0],	# 9x9
		   [0,0,0,0,0,0,0,0,0],
		   [0,0,0,0,0,0,0,0,0],
		   [0,0,0,0,0,0,0,0,0],
		   [0,0,0,0,0,0,0,0,0],
		   [0,0,0,0,0,0,0,0,0],
		   [0,0,0,0,0,0,0,0,0],
		   [0,0,0,0,0,0,0,0,0],
		   [0,0,0,0,0,0,0,0,0]]

	duration = rowGenerator(board) # generate the full board
	print("Generation time: {} seconds\n".format(round(duration,10))) # print the generation time of the board
	difficulty = inputHandler("Select the difficulty of the game: \n0- Easy \n3- Medium \n5- Hard\n",[0,3,5]) # prompt for difficulty
	printBoard(troubleMaker(board,difficulty)) # generate the question board and print it
	if inputHandler("Show the answer? 1-Yes ",[1]): # prompt for answer
		printBoard(board) # print the original(full) board

main()