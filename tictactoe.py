import time
import board, ai

def player_move(player, opponent, difficulty, game_round):
	# Gets move parameter from the Human Player, checks its correctness and availability and inserts on board
	print ("You\'re playing with", player)
	while True:
		move_par = int(input ("Your move parameters: "))
		if board.check_move_par_correctness(move_par) and board.check_move_par_occupied(move_par):
			break
	board.move_insertion(player, move_par)

def computer_move(player, opponent, difficulty, game_round):
	# Cheks difficulty correctness and launches AI
	available_difficulties = [1, 2, 3, 4]
	if difficulty in available_difficulties:
		ai.computer_move_difficulty(player, opponent, difficulty, game_round)
	else:
		print ("Wrong difficulty.")
		import sys
		sys.exit()

def game_start():
	global party_map
	party_map = ""
	single_start_time = time.time()
	board.board_cleaning()
	for game_round in range(1,10):
		if game_round % 2 != 0:
			player = "O"
			opponent = "X"
			computer_move(player, opponent, 4, game_round)
		else:
			player = "X"
			opponent = "O"
			computer_move(player, opponent, 2, game_round)
		if info_mode:
			board.board_printing(game_round)
		party_map = party_map+str(board.last_move)
		if board.result_checking():
			if info_mode:
				print ("\"", player, "\"", " won in ", game_round, " moves.", sep="")
				# if player == "O":
				# 		sys.exit()
			winner = player
			break
		elif game_round == 9 and board.result_checking() == False:
			if info_mode:
				print ("Draw")
			winner = "D"
	game_end(winner, game_round, single_start_time)

def game_end(winner, game_round, single_start_time):
	single_game_time = time.time() - single_start_time
	saving_results(winner, game_round, single_game_time)

def saving_results(winner, game_round, single_game_time):
	results_file.write(winner+":"+str(game_round)+":"+str(single_game_time)+":"+party_map+":"+board.winning_combination+"\n")

def file_preparation():
	global results_file
	file_path = "wyniki.txt"
	results_file = open(file_path, "w")

total_start_time = time.time()
print ("")
file_preparation()
#Information mode [True, False]
info_mode = True
for i in range(10):
	game_start()
results_file.close()
total_game_time = time.time() - total_start_time
if info_mode:
	print ("Done in", round(total_game_time,5), "seconds.")
	print ("Zrobilem", ai.ile_forkow, "forkow i", ai.ile_blokad_forkow1, "blokad #1 i", ai.ile_blokad_forkow2, "blokad #2")
