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

def player_move(player, opponent, difficulty):
	global move_par
	print ("You\'re playing with", player)
	while True:
		move_par = int(input ("Your move parameters: "))
		if check_move_par_correctness(move_par) and check_move_par_occupied(move_par):
			break
	move_insertion(player, move_par)

def computer_move(player, opponent, difficulty):
	global inserted
	inserted = False
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
#			if inserted == True and result_checking() == True:
#				print ("Wstawione i wygrane - sie nie zdarza")
#			if inserted == True and result_checking() == False:
#				print ("Wstawione - uniknal porazki")
			if inserted == False:
				computer_move_difficulty_1(player)
	elif difficulty == 4:
		computer_move_difficulty_2(player)
		if result_checking() == False:
			computer_move_difficulty_3(player, opponent)
			if inserted == False:
				computer_move_difficulty_4(player)
	elif difficulty == 5:
		computer_move_difficulty_2(player)
		if result_checking() == False:
			computer_move_difficulty_3(player, opponent)
			if inserted == False:
				computer_move_difficulty_5(player)
	else:
		print ("Wrong difficulty.")
		sys.exit()

def computer_move_difficulty_1(player):
	#AI - randomized moves
	global move_par
	while True:
		move_par = random.randrange(1,10)
		if board.get(move_par,0) == " ":
			move_insertion(player, move_par)
			break

def computer_move_difficulty_2(player):
	#Tries to win in one move
	global move_par
	if game_round >= 5:
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
	#Blocks opponent from winning in one move
	global move_par, inserted
	if game_round >= 4:
		for move_par in range(1, 10):
			if board.get(move_par,0) == " ":
				move_insertion(opponent, move_par)
				if result_checking():
					#Solution found
					move_insertion(player, move_par)
					inserted = True
					break
				else:
					#No result, reversing change
					move_insertion(" ", move_par)
					if move_par == 9:
						inserted = False	

def computer_move_difficulty_4(player):
	global move_par, inserted, move_to_third_preference, temp
	temp = 0
	second_preference = (1, 3, 7, 9)
	third_preference = (2, 4, 6, 8)
	move_to_third_preference = False
	temp_random = []

	if board.get(5, "0") == " ":
		move_par = 5
		move_insertion(player, move_par)
	else:
		while True:
			
			if move_to_third_preference and game_round > 3:
				move_par = third_preference[random.randrange(0,4)]
				print ("Pref 3. Ruch:", move_par)
			else:
				move_par = second_preference[random.randrange(0,4)]
				print ("Pref 2. Ruch:", move_par)

			if temp == 3:
				print ("Ruch po 3 iteracjach AI")
				if move_to_third_preference == True:
					move_insertion(player, move_par) #robiony ruch
				elif game_round >= 8 and move_to_third_preference == False:
					move_insertion(player, move_par)
					return 0
				else:
					move_par = third_preference[random.randrange(0,4)]
					temp = 0
					if computer_move_one_ahead(player, move_par) and board.get(move_par, "0") == " ":
						move_insertion(player, move_par) #robiony ruch
						return 0
					else:
						temp = 0
						continue
			if board.get(move_par, "0") == " ":
				if game_round > 2 and game_round < 9:
					if computer_move_one_ahead(player, move_par):
						move_insertion(player, move_par) #robiony ruch
						break
				else:
					move_insertion(player, move_par)
					break
			else:

				#best_fields[move_par] = True
				print ("Pole zajete")
				if (((board[second_preference[0]] == " ") and (board[second_preference[1]] == " ")) or
				 	((board[second_preference[0]] == " ") and (board[second_preference[2]] == " ")) or
				 	((board[second_preference[0]] == " ") and (board[second_preference[3]] == " ")) or
				 	((board[second_preference[1]] == " ") and (board[second_preference[2]] == " ")) or
				 	((board[second_preference[1]] == " ") and (board[second_preference[3]] == " ")) or
				 	((board[second_preference[2]] == " ") and (board[second_preference[3]] == " "))) == False:
					print ("Nie ma wiecej wolnych pol z 2 pref")
					while True:
						move_par = third_preference[random.randrange(0,4)]
						move_to_third_preference = True
						print ("Wylosowalem", move_par)
						if game_round == 9:
							for move_par in range(1,10):
								if board.get(move_par, "0") == " ":
									move_insertion(player, move_par)
									return 0
						if board.get(move_par, "0") == " ":
							move_insertion(player, move_par)
							return 0

def computer_move_one_ahead(player, move_par):
	global board2, temp
	board2 = board.copy()
	board2[move_par] = player

	print ("Wylosowalem", move_par, "Wchodzi AI w rundzie", game_round)
	for move2_par in range (1,10):
		if board2.get(move2_par,0) == " ":
			print ("Wstawiam roboczo", move2_par)
			board2[move2_par] = player
			if result2_checking() == True:
				print ("zaakceptowano", move_par, "bo hula z", move2_par)
				return True
			else:
				board2[move2_par] = " "
				#print ("AI nic nie wylosowalo")
				#return "End"
	temp = temp + 1

def computer_move_difficulty_5(player):
	global move_par
	force_first = False
	first_preference = (1, 3, 7, 9)
	second_preference = (5, 5, 5, 5)
	third_preference = (2, 4, 6, 8)
	if game_round <= 4:
		preference = first_preference
	elif game_round == 5:
		preference = second_preference
	else:
			preference = third_preference

	while True:
		if force_first == True:
			preference = first_preference
		move_par = preference[random.randrange(0,4)]
		if board.get(move_par, "0") == " ":
			move_insertion(player, move_par)
			break
		else:
			if ((game_round >=6) and 
				(board[third_preference[0]] != " ") and
				(board[third_preference[1]] != " ") and
				(board[third_preference[2]] != " ") and
				(board[third_preference[3]] != " ")):
				force_first = True				

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

def result2_checking():
	if (((board2[1] == board2[2] == board2[3]) and (board2.get(1) != " ")) or
	((board2[4] == board2[5] == board2[6]) and (board2.get(4) != " ")) or
	((board2[7] == board2[8] == board2[9]) and (board2.get(7) != " ")) or
	((board2[1] == board2[4] == board2[7]) and (board2.get(1) != " ")) or
	((board2[2] == board2[5] == board2[8]) and (board2.get(2) != " ")) or
	((board2[3] == board2[6] == board2[9]) and (board2.get(3) != " ")) or
	((board2[1] == board2[5] == board2[9]) and (board2.get(1) != " ")) or
	((board2[3] == board2[5] == board2[7]) and (board2.get(3) != " "))):
		return True

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
			computer_move(player, opponent, 1)
		else:
			player = "X"
			opponent = "O"
			computer_move(player, opponent, 4)
		if info_mode:
			board_printing()
		party_map = party_map+str(move_par)
		if result_checking():
			if info_mode:
				print ("\"", player, "\"", " won in ", game_round, " moves.", sep="")
				#if player == "O":
				#	sys.exit()
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
#Selection of difficulty mode [1, 2, 3, 4]
#difficulty = 4
#Information mode [True, False]
info_mode = True
for i in range(100):
	game_start()
	#computer_move_difficulty_4("O")
results_file.close()
total_game_time = time.time() - total_start_time
if info_mode:
	print ("Done in", round(total_game_time,5), "seconds.")

