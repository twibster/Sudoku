from time import time
import numpy as np

# board generation functions
def boardGenerator(board):
	start=time() #calculate the time required to generate the board
	state,row= rowGenerator(board,0) # call the row generator function
	while not state: # if the fail-safe variable is triggered
		clearRow(row-1,board) # clear the previous row
		state,row = rowGenerator(board,row-1) # start from the previous row
	return time()-start

def rowGenerator(board,start):
	failSafe=0 # a variable used to abandon the current row (3x3 square keeps preventing the generation process)
	for row in range(start,9):
		while not columnGenerator(row,board): # keep clearing the row until a combination is valid
			clearRow(row,board)
			failSafe +=1
			if failSafe==20: # if the combinations used exceeds the limit
				return 0,row # retreat to the previous row
	return 1,None

def columnGenerator(row,board):
	for col in range(9): # loop over the columns 
		num = np.random.randint(1,10) # generate random number
		forbid=[] # this list is used to prevent using an invalid number more than once
		while checkValid(num,row,col,board):
			forbid.append(num) # add the number to the list of forbidden numbers
			num=np.random.randint(1,10)
			while num in forbid: # keep generating random numbers until the number is not forbidden 
				if len(forbid)==9: # if all 9 numbers are invalid (the whole row must be cleared and the process must start over)
					return 0
				num=np.random.randint(1,10) # generate another number
		board[row][col]=num # finally, if the number is valid, add it to the board
	return 1

#functions that check the validity of the generated number
def checkValid(number,row,col,board):
	'''this function checks the validity of a given number by iterating over the the board in a 'T' like pattern '''
	for ro in range(9):  # loop over all the rows 
		if ro ==row: # check if the current is row the row of the provided number
			for num in board[ro]: # loop through each number in the row
				if num == number: # check if there is a number equal to the provided number in the row
					return 1
		if ro == row +1 or ro== row+2: #check the 3x3 square around the number
			if number in squareFinder(board,row,col):
				return 1
		if board[ro][col] ==number: # check if the number is equal to the provided number in the provided column
			return 1
	return 0

def squareFinder(board,row,col):
	'''this function gets the 3x3 square of numbers surrounding a given index'''
	rowStart,rowEnd=indicesFinder(row)
	colStart,colEnd=indicesFinder(col)
	return board[rowStart:rowEnd,colStart:colEnd] #return the 3x3 square

def indicesFinder(ref):
	'''this functions returns the start and end indices of the required square surrounding a given index'''
	if ref in [2,5,8]:
		return ref-2, ref+1
	if ref in [1,4,7]:
		return ref-1,ref+2
	if ref in [0,3,6]:
		return ref,ref+3

#fail-safe function
def clearRow(row,board):
	for col in range(9):
		board[row][col]=0 # clear the specified row

# question board generation function
def troubleMaker(board,difficulty):
	'''this function is used to create the question board by clearing random places in the board'''
	troubledBoard = board.tolist() # the board array is converted to a list so that strings can be used (a deep copy was used earlier but later .tolist method is used to create a deep copy)
	for row in range(9):
		emptyPlaces = np.random.randint(difficulty,difficulty+4) # generate a random number of empty places for each row
		emptyCols=[] # this list is used so that a previously empty place does not change again instead of another one
		while emptyPlaces>0:
			col=np.random.randint(0,9) # generate a random col (random number for the empty place ie. its position)
			while col in emptyCols:
				col =np.random.randint(0,9)
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

# board output
def boardPrinter(board):
	print("\n\t-------------------------")
	for row in range(9):
		print(f"\t| {' '.join(map(str,board[row][:3]))} | " + # .join is used to clear the commas and the brackets
			  f"{' '.join(map(str,board[row][3:6]))} | "   +
			  f"{' '.join(map(str,board[row][6:9]))} | ") 
		if row in [2,5,8]: # add the bottom border
			print("\t-------------------------")

# no brainer
def main():
	failCounter=0 #counts the amount of times a number is flagged as an invalid option
	board=np.zeros((9,9), dtype=int) #9x9 array
	duration = boardGenerator(board) # generate the full board
	print("\t\tGeneration time: {} seconds\n".format(round(duration,10))) # print the generation time of the board
	difficulty = inputHandler(" Select the difficulty of the game: \n\n 0- Easy \n 3- Medium \n 5- Hard\n\n ",[0,3,5]) # prompt for difficulty
	boardPrinter(troubleMaker(board,difficulty)) # generate the question board and print it
	if inputHandler("\n Show the answer? 1-Yes ",[1]): # prompt for answer
		boardPrinter(board) # print the original(full) board

main()