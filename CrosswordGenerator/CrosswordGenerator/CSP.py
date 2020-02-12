import re
import random
import os
import time
from constraint import Problem
from constraint import AllDifferentConstraint
# Remove the dot from this import to run the console version of the program
from .Board import Board


# Generate a crossword board with some width and height
def generate_board(width, height):
	board = Board(width)

	for i in range(0, height):
		for j in range(0, width):
			if not random.randint(0, 2):
				board.set_grid(i, j, 0)

	# Remove any locked-in white tiles
	for i in range(0, height):
		for j in range(0, width):
			# If the current column is black, stop.
			if(board.get_tile(i, j) == 0):
				continue
			# If box is in one of the corners, edge cases.
			elif(corner_checker(i, j, height, width, board)):
				changing_tile(i, j, board)
			# If two black boxes on each horizontal side of the white box.
			elif(j != 0 and j + 1 != width and check_sides_hori(i, j, board)):
				if((i == 0 and board.get_tile(i + 1, j) == 0) or (i == height - 1 and board.get_tile(i - 1, j) == 0)
					or check_sides_verti(i, j, width, board)):
					changing_tile(i, j, board)
			# If two black boxes on each vertical side of the white box.
			elif(i != 0 and i + 1 != height and check_sides_verti(i, j, width, board)):
				if((j == 0 and board.get_tile(i, j + 1 ) == 0) or (j == width - 1 and board.get_tile(i, j - 1 ) == 0)):
					changing_tile(i, j, board)
	return board

# Change current tile from white to black
def changing_tile(i, j, board):
	board.set_grid(i, j, 0)	

def check_sides_hori(i, j, board):
	return (board.get_tile(i, j - 1) == 0 and board.get_tile(i, j + 1) == 0)

def check_sides_verti(i, j, width, board):
	return (i != 0 and i + 1 != width and board.get_tile(i - 1, j) == 0 and board.get_tile(i + 1, j) == 0)

# Edge cases in the corner
def corner_checker(i, j, height, width, board):
	if (i == 0 and board.get_tile(i + 1, j) == 0):
		# (0,0)
		if(j == 0):
			return (board.get_tile(i, j + 1) == 0)
		# (0, width)
		elif(j + 1 == width):
			return (board.get_tile(i, j - 1) == 0)

	elif (i == height - 1 and board.get_tile(i - 1, j) == 0):
		# (height, 0)
		if(j == 0):
			return (board.get_tile(i, j + 1) == 0)
		# (height, width)
		elif(j + 1 == width):
			return (board.get_tile(i, j - 1) == 0)


# List of horizontal words in the grid
def get_h_list(width, height, board):
	# List of horizontal words: their start position and their length -> (x, y), length
	horiVal = []

	# To insert the value at the correct index in the list
	done = 0
	for i in range(0, height):
		horiLength = 0
		val = ''
		insert = False
		for j in range(0, width):
			# If the current box is black
			if(board.__grid__[i][j] == 0):
				# If the word is long enough, we want to add it to the list
				if(1 < horiLength):
					insert = True
				else:
					horiLength = 0
			# Checking for words that end not with a box but with boarder
			if(j + 1 == width  and 0 < horiLength and board.__grid__[i][j] == 1):
				horiLength += 1
				insert = True
				

			# To get the start placement of the index 
			elif(horiLength == 0  and board.__grid__[i][j] == 1):
				val = '(' + str(j) + ', ' + str(i) + ')'

			# Is the word finished and of correct size, insert it into the array
			if insert:
				horiVal.insert(done, "H: "+ val + ", " + str(horiLength))
				horiLength = 0
				done += 1
				insert = False
				val = ''

			# Else we increase the current length
			elif(board.__grid__[i][j] == 1):
				horiLength += 1

	return horiVal


# List of vertical words in the grid
def get_v_list(width, height, board):
	vertiVal = []

	# To insert the value at the correct index
	done = 0
	for i in range(0, height):
		vertiLength = 0
		val = ''
		insert = False
		for j in range(0, width):
			# If the current box is black
			if(board.__grid__[j][i] == 0):
				# If the word is long enough, we want to add it to the list
				if(1 < vertiLength):
					insert = True
				else:
					vertiLength = 0
			# Checking for words that end not with a box but with border
			if(j + 1 == width  and 0 < vertiLength and board.__grid__[j][i] == 1):
				vertiLength += 1
				insert = True
				

			# To get the start placement of the index 
			elif(vertiLength == 0  and board.__grid__[j][i] == 1):
				val = '(' + str(i) + ', ' + str(j) + ')'

			# Is the word finished and of correct size, input it into the array
			if insert:
				vertiVal.insert(done, "V: "+ val + ", " + str(vertiLength))
				vertiLength = 0
				done += 1
				insert = False
				val = ''

			elif(board.__grid__[j][i] == 1):
				vertiLength += 1

	return vertiVal


# Get the word data from file, and put int a dict
def get_words(path):
	word_list = dict()
	entry = 0
	word = ""
	with open(path, 'r', encoding='utf8') as file:
		for line in file:
			line = line.strip()
			# Set the word as the key.
			if entry == 0:
				word = line
				word_list[word] = []
				entry += 1
			# Add frequency to the word's list.
			elif entry == 1:
				word_list[word].append(int(line))
				entry += 1
			# Add normalized frequency to the word's list.
			elif entry == 2:
				word_list[word].append(float(line))
				entry += 1
			# Add definition to the word's list.
			elif entry == 3:
				word_list[word].append(line)
				entry = 0
	return word_list

# Sort words into segregated lists of the same word length.
def get_word_lengths(words):
	words_len = []
	for _ in range(0, 50):
		words_len.append([])
	for w in words:
		words_len[len(w)].append(w)

	return words_len

# A very simple difficulty heuristic, returning only solutions
# that fit into the chosen difficulty range (easy, medium or hard),
# defined by the mean frequency of the words in the puzzle.
def difficulty(solutions, diff, words):

	# If none of these was chosen, return all solutions.
	if diff != 'easy' and diff != 'medium' and diff != 'hard':
		return solutions

	diff_solutions = []

	for solution in solutions:

		# Find the mean frequency of words for this solution.
		total_freq = 0
		for word in list(solution.values()):
			total_freq += words[word][0]
		sol_freq = total_freq / len(solution)

		# Filter out unwanted solutions.
		if diff == 'easy' and sol_freq >= 10000:
			diff_solutions.append(solution)

		elif diff == 'medium' and sol_freq >= 5000 and sol_freq < 10000:
			diff_solutions.append(solution)

		elif diff == 'hard' and sol_freq < 5000:
			diff_solutions.append(solution)

	return diff_solutions


# Function to define variable constraints.
def equal_char(char1, char2):
	def voodoo(word1, word2):
		return word1[char1] == word2[char2]
	return voodoo


# Generates solutions given a board and word list.
def generate_solutions(height, width, board, words, word_lengths):
	
	problem = Problem()

	h_list = get_h_list(width, height, board)
	v_list = get_v_list(width, height, board)

	# Set the domains of variables and add them to the problem.
	for var in (h_list + v_list):
		var_len = int(re.findall(r'[0-9]+$', var)[0])
		problem.addVariable(var, word_lengths[var_len])

	# Iterate over all horizontal variables.
	for h_var in h_list:
		h_at = [int(i) for i in re.findall(r'[0-9]+', h_var)]
		# Iterate over all vertical variables.
		for v_var in v_list:
			v_at = [int(i) for i in re.findall(r'[0-9]+', v_var)]
			# Iterate over each char location in each horizontal variable.
			for h_char in range(h_at[0], h_at[0] + h_at[2]):
				cont = True
				# Iterate over each char location in each vertical variable.
				for v_char in range(v_at[1], v_at[1] + v_at[2]):
					# If the variables intersect, add a constraint.
					if h_char == v_at[0] and v_char == h_at[1]:
						problem.addConstraint(
							equal_char(h_char - h_at[0], v_char - v_at[1]),
							[h_var, v_var])
						cont = False
						break
				if not cont:
					break

	# Let no two variables have the same word.
	problem.addConstraint(AllDifferentConstraint())

	return problem.getSolutions()

# Generates a board, returning it with a solution.
# Failing this, it calls itself again, generating a new board.
def make_full_board(height, width, diff, words, word_lengths):

	time_start = time.time()

	board = generate_board(width, height)

	# Information to the console:
	print("\nBoard generated:")
	for row in board.get_grid():
		for col in row:
			if col:
				print("_ ", end='')
			else:
				print("# ", end='')
		print()
	print("\nChecking for solution...")

	solutions = generate_solutions(height, width, board, words, word_lengths)
	solutions = difficulty(solutions, diff, words)

	# Informing the console and recursively calling itself if no solution
	# exists for the generated board (using the given wordlist).
	if not solutions:
		time_taken = time.time() - time_start
		print("\nGenerating this", str(width) + "x" + str(height), diff,
			  "failure took", str(time_taken), "seconds.")
		print("\nNo solutions.")
		return make_full_board(width, height, diff, words, word_lengths)
	print("\n%d solutions." % len(solutions))

	board.set_solution(solutions[random.randint(0, len(solutions) - 1)])

	# Adding the list of hints to the board.
	if board.get_solution():
		hints = dict()
		for key in board.get_solution():
			hints[key] = words[board.get_solution()[key]][2]

		board.set_hint_list(hints)

	return board

# Effectively a wrapper for make_full_board, takes the word list from
# a file and saves it to memory.
def get_full_board(width, height, diff):

	# Time how quickly a crossword is generated.
	time_start = time.time()

	file_path = os.path.relpath('word_lists/combined_word_data.txt', '..')

	# Fetch the word data.
	words = get_words(file_path)
	word_lengths = get_word_lengths(words)

	board = make_full_board(width, height, diff, words, word_lengths)

	# Print the time it took to generate a crossword.
	time_taken = time.time() - time_start
	print("\nGenerating this", str(width) + "x" + str(height), diff,
		  "crossword took", str(time_taken), "seconds.\n")

	return board

# The following are helper functions for the view
def get_hints_pos(board):
	hints = board.get_hint_list().keys()
	#H: (1, 2), 2
	matches = re.findall(r'(\d,\s\d)', str(hints))
	hints = list()
	for match in matches:
		hints.append(match.split(', '))
	return hints

def get_orientation(board):
	orientation = board.get_hint_list().keys()
	matches = re.findall(r'[A-Z]', str(orientation))
	return matches

# The main function, used for testing
def main():
	get_full_board(5, 5, 'easy')
	return

if __name__ == "__main__":
	main()