#!/usr/local/bin/python3
import time, logging, getopt, sys
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
			player_move(player, opponent, difficulty_level, game_round)
		else:
			player = "X"
			opponent = "O"
			computer_move(player, opponent, difficulty_level, game_round)
		if info_mode:
			board.board_printing(game_round)
		else:
			# Turn off to increase the program performance (3x higher speed)
			board.board_printing_debug(game_round)
		party_map = party_map+str(board.last_move)
		if board.result_checking():
			if info_mode:
				print ("\"", player, "\"", " won in ", game_round, " moves.", sep="")
				# if player == "O":
				# 		sys.exit()
			else:
				logging.info("Player \""+str(player)+"\""+" won in "+str(game_round)+" moves.")
			winner = player
			break
		elif game_round == 9 and board.result_checking() == False:
			if info_mode:
				print ("Draw")
			else:
				logging.info("Draw")
			winner = "D"
	game_end(winner, game_round, single_start_time)

def game_end(winner, game_round, single_start_time):
	single_game_time = time.time() - single_start_time
	saving_results(winner, game_round, single_game_time)
	if game_played == games_played_total:
		# Checking for the final game round
		results_file.close()
		total_game_time = time.time() - total_start_time
		logging.info("Total game time: " + str(round(total_game_time,5)) + " seconds")
		logging.info("Forks made: " + str(ai.ile_forkow))
		logging.info("Single forks prevented: " + str(ai.ile_blokad_forkow1))
		logging.info("Double forks prevented: " + str(ai.ile_blokad_forkow2))

def saving_results(winner, game_round, single_game_time):
	results_file.write(winner+":"+str(game_round)+":"+str(single_game_time)+":"+party_map+":"+board.winning_combination+"\n")

def file_preparation():
	global results_file
	file_path = "wyniki.txt"
	results_file = open(file_path, "w")

def main(argv):
	global debug_mode, games_played_total, info_mode, difficulty_level
	debug_mode = False
	games_played_total = 1
	info_mode = True
	difficulty_level = 4
	try:
		opts, args = getopt.getopt(argv,"hg:d:",["debug", "silent", "difficulty=", "games="])
	except getopt.GetoptError:
		print ("""tictactoe.py -
-h : list of available options  
-g <number> : number of games
-d <number> : AI difficulty of [1 - easy, 2 - medium, 3 - hard, 4 - unbeatable] 
--debug : debug mode
--silent : silent mode""")
		sys.exit(2)
	for opt, arg in opts:
		if opt == '-h':
			print ("""tictactoe.py -
-h : list of available options  
-g <number> : number of games
-d <number> : AI difficulty of [1 - easy, 2 - medium, 3 - hard, 4 - unbeatable] 
--debug : debug mode
--silent : silent mode""")
			sys.exit()
		elif opt in ("--debug"):
			debug_mode = True
			info_mode = False
		elif opt in ("--silent"):
			info_mode = False
			debug_mode = False
		elif opt in ("-d", "--difficulty"):
			print ("BYLEM TUTAJ")
			difficulty_level = int(arg)
		elif opt in ("-g", "--games"):
			games_played_total = int(arg)

if __name__ == "__main__":
   main(sys.argv[1:])

if debug_mode:
	logging.basicConfig(level=logging.DEBUG, format="-%(levelname)s- %(message)s")
	logging.debug("Debug mode: " + str(debug_mode))
	logging.debug("Silent mode: " + str(info_mode))
	logging.debug("Total number of games to play: " + str(games_played_total))
	logging.debug("AI difficulty level: " + str(difficulty_level))
else:
	logging.disable(logging.CRITICAL)


total_start_time = time.time()

file_preparation()
for game_played in range(1, games_played_total+1):
	logging.debug("Game number: " + str(game_played))
	game_start()
