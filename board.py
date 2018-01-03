import logging

def board_cleaning():
	# Cleaning board after the previous game round
	global board
	board = {}
	for field in range(1,10):
		board[field] = " "

def board_printing(game_round):
	# Printing the game board
	print (("Round "+str(game_round)).center(13,"-"))
	print ("-------------")
	print ("|", board[1], "|", board[2], "|", board[3], "|")
	print ("-------------")
	print ("|", board[4], "|", board[5], "|", board[6], "|")
	print ("-------------")
	print ("|", board[7], "|", board[8], "|", board[9], "|")
	print ("-------------")

def check_move_par_correctness(move_par):
	if move_par in board.keys():
		return True
	else:
		print ("There is no such a field on the board.")
		return False

def check_move_par_occupied(move_par):
	if board[move_par] == " ":
		return True
	else:
		# print ("The field is already occupied.")
		return False

def result_checking():
	global winning_combination
	winning_combination = ""
	if (board[1] == board[2] == board[3]) and (board[1] != " "):
		winning_combination = "123"
		return True
	elif (board[4] == board[5] == board[6]) and (board[4] != " "):
		winning_combination = "456"
		return True
	elif (board[7] == board[8] == board[9]) and (board[7] != " "):
		winning_combination = "789"
		return True
	elif (board[1] == board[4] == board[7]) and (board[1] != " "):
		winning_combination = "147"
		return True
	elif (board[2] == board[5] == board[8]) and (board[2] != " "):
		winning_combination = "258"
		return True
	elif (board[3] == board[6] == board[9]) and (board[3] != " "):
		winning_combination = "369"
		return True
	elif (board[1] == board[5] == board[9]) and (board[1] != " "):
		winning_combination = "159"
		return True
	elif (board[3] == board[5] == board[7]) and (board[3] != " "):
		winning_combination = "357"
		return True
	else:
		return False

def move_insertion(player, move_par):
	global last_move
	board[move_par] = player
	last_move = move_par

def board_printing_debug(game_round):
	# Turn off to increase the program performance (3x higher speed)
	logging.info(("Round "+str(game_round)).center(13,"-"))
	logging.info("-------------")
	logging.info("| "+str(board[1])+" | "+str(board[2])+" | "+str(board[3])+" |")
	logging.info("-------------")
	logging.info("| "+str(board[4])+" | "+str(board[5])+" | "+str(board[6])+" |")
	logging.info("-------------")
	logging.info("| "+str(board[7])+" | "+str(board[8])+" | "+str(board[9])+" |")
	logging.info("-------------")