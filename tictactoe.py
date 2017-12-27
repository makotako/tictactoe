import random, time, os, sys

def board_cleaning():
	global board
	board = {
		1:" ", 2:" ", 3:" ",
		4:" ", 5:" ", 6:" ",
		7:" ", 8:" ", 9:" "}
	return 0

def board_printing():
	global game_round
	print (("Round "+str(game_round)).center(13,"-"))
	print ("-------------")
	print ("|", board[1], "|", board[2], "|", board[3], "|")
	print ("-------------")
	print ("|", board[4], "|", board[5], "|", board[6], "|")
	print ("-------------")
	print ("|", board[7], "|", board[8], "|", board[9], "|")
	print ("-------------")

def player_move(symbol):
	print ("You\'re playing with", symbol)
	while True:
		move_par = int(input ("Your move parameters: "))
		if check_move_par_correctness(move_par) and check_move_par_occupied(move_par):
			break
	move_insertion(symbol, move_par)

def computer_move(player, opponent):
	if difficulty == 1:
		computer_move_difficulty_1(player)
	elif difficulty == 2:
		computer_move_difficulty_2(player)
		if result_checking() == False:
			computer_move_difficulty_1(player)
	elif difficulty == 3:
		computer_move_difficulty_2(player)
		if result_checking() == False:
			computer_move_difficulty_3(player, opponent)
		if result_checking() == False:
			computer_move_difficulty_1(player)
	else:
		print ("Wrong difficulty.")
		sys.exit()
	move_insertion(player, move_par)

def computer_move_difficulty_1(player):
	global move_par
	while True:
		move_par = random.randrange(1,10)
		if board.get(move_par,0) == " ":
			break

def computer_move_difficulty_2(player):
	global move_par
	for move_par in range(1, 10):
		if board.get(move_par,0) == " ":
			move_insertion(player, move_par)
			if result_checking():
				#Solution found
				break
			else:
				#No result, reversing change
				move_insertion(" ", move_par)

def computer_move_difficulty_3(player, opponent):
	global move_par
	for move_par in range(1, 10):
		if board.get(move_par,0) == " ":
			move_insertion(opponent, move_par)
			if result_checking():
				#Solution found
				#move_insertion(player, move_par)
				break
			else:
				#No result, reversing change
				move_insertion(" ", move_par)

def check_move_par_correctness(move_par):
	if move_par in board.keys():
		return True
	else:
		print ("There is no such a field on the board.")

def check_move_par_occupied(move_par):
	if board.get(move_par,0) == " ":
		return True
	else:
		print ("The field is already occupied.")

def move_insertion(symbol, move_par):
	board[move_par] = symbol

def result_checking():
	global winning_combination
	winning_combination = ""
	if (board[1] == board[2] == board[3]) and (board.get(1) != " "):
		winning_combination = "123"
		return True
	elif (board[4] == board[5] == board[6]) and (board.get(4) != " "):
		winning_combination = "456"
		return True
	elif (board[7] == board[8] == board[9]) and (board.get(7) != " "):
		winning_combination = "789"
		return True
	elif (board[1] == board[4] == board[7]) and (board.get(1) != " "):
		winning_combination = "147"
		return True
	elif (board[2] == board[5] == board[8]) and (board.get(2) != " "):
		winning_combination = "258"
		return True
	elif (board[3] == board[6] == board[9]) and (board.get(3) != " "):
		winning_combination = "369"
		return True
	elif (board[1] == board[5] == board[9]) and (board.get(1) != " "):
		winning_combination = "159"
		return True
	elif (board[3] == board[5] == board[7]) and (board.get(3) != " "):
		winning_combination = "357"
		return True
	else:
		return False

def game_start():
	global game_round, party_map
	game_round = 0
	party_map = ""
	single_start_time = time.time()
	board_cleaning()
	for game_round in range(1,10):
		if game_round % 2 != 0:
			player = "O"
			opponent = "X"
		else:
			player = "X"
			opponent = "O"
		computer_move(player, opponent)
		if info_mode:
			board_printing()
		party_map = party_map+str(move_par)
		if result_checking():
			if info_mode:
				print ("\"", player, "\"", " won in ", game_round, " moves.", sep="")
			winner = player
			break
		elif game_round == 9 and result_checking() == False:
			if info_mode:
				print ("Draw")
			winner = "D"
	game_end(winner, game_round, single_start_time)

def game_end(winner, game_round, single_start_time):
	single_game_time = time.time() - single_start_time
	saving_results(winner, game_round, single_game_time)

def saving_results(winner, game_round, single_game_time):
	results_file.write(winner+":"+str(game_round)+":"+str(single_game_time)+":"+party_map+":"+winning_combination+"\n")

def file_preparation():
	global results_file
	file_path = "wyniki.txt"
	results_file = open(file_path, "w")

total_start_time = time.time()
print ("")
file_preparation()
difficulty = 3
info_mode = True
for i in range(1):
	game_start()
results_file.close()
total_game_time = time.time() - total_start_time
if info_mode:
	print ("Done in", round(total_game_time,5), "seconds.")

