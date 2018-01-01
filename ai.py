import random
import board

inserted = False
fork_field_for_blok = []
ile_forkow = 0
ile_blokad_forkow1 = 0
ile_blokad_forkow2 = 0

def computer_move_difficulty(player, opponent, difficulty, game_round):
	# Makes computer move according to the selected difficulty level
	if difficulty == 1:
		computer_move_difficulty_1(player)
	elif difficulty == 2:
		computer_move_difficulty_2(player, opponent, game_round)
		if inserted == False:
			computer_move_difficulty_1(player)
	elif difficulty == 3:
		computer_move_difficulty_2(player, opponent, game_round)
		if inserted == False:
			computer_move_difficulty_3(player, game_round)
			if inserted == False:
				computer_move_difficulty_1(player)
	elif difficulty == 4:
		computer_move_difficulty_2(player, opponent, game_round)
		if inserted == False:
			computer_move_difficulty_3(player, game_round)
			if inserted == False:
				computer_move_difficulty_4(player, opponent, game_round)

def computer_move_difficulty_1(player):
	# AI with randomized moves
	global move_par
	while True:
		move_par = random.randint(1,9)
		if board.check_move_par_occupied(move_par):
			board.move_insertion(player, move_par)
			break

def computer_move_difficulty_2(player, opponent, game_round):
	# AI skilled to win with one move and prevent lose in one move
	global inserted
	inserted = False
	#Tries to win in one move
	if game_round >= 5:
		for move_par in range(1, 10):
			if board.check_move_par_occupied(move_par):
				board.move_insertion(player, move_par)
				#last_move = move_par
				if board.result_checking():
					#Solution found
					inserted = True
					return True
				else:
					#Player has not possible win, reversing change
					board.move_insertion(" ", move_par)
	#Blocks opponent from winning in one move
	if game_round >= 4 and inserted == False:
		for move_par in range(1, 10):
			if board.check_move_par_occupied(move_par):
				board.move_insertion(opponent, move_par)
				if board.result_checking():
					# Solution found
					board.move_insertion(player, move_par)
					inserted = True
					return True
				else:
					# Opponent has not possible win, reversing change
					board.move_insertion(" ", move_par)
					if move_par == 9:
						inserted = False

def computer_move_difficulty_3(player, game_round):
	# AI creating forks
	global inserted
	if game_round > 3:
		find_fork_available_rows(player, "fork_create")
	else:
		inserted = False

def find_fork_available_rows(player, purpose):
	# Search for fork possibilities.
	# Prepare list of rows that contain only one Player's symbol (fork criteria)
	rows = [[1, 2, 3], [4, 5, 6], [7, 8, 9],
		[1, 4, 7], [2, 5, 8], [3, 6, 9],
		[1, 5, 9], [3, 5, 7]]
	rows_fork_available = []
	for single_row in rows:
		#print (single_row, end="")
		single_row_content = []
		for single_row_field in single_row:
			single_row_content.append(board.board[single_row_field])
		#print (single_row_content)
		if single_row_content.count(player) == 1 and single_row_content.count(" ") == 2:
			rows_fork_available.append(single_row)
	#print ("Rows qualified", rows_fork_available)
	if purpose == "many_forks":
		return rows_fork_available
	else:
		find_fork_overlaping_rows(rows_fork_available, player, purpose)

def find_fork_overlaping_rows(rows_fork_available, player, purpose):
	# Prepares the rows that meet fork criteria and overlap
	global inserted, move_par, overlaping_field, ile_forkow
	overlaping_field = 0
	for first_row in rows_fork_available:
		#print ("\n Dla wiersza:", first_row)
		for second_row in rows_fork_available:
			if second_row != first_row:
				#print (second_row)
				for first_row_element in first_row:
					if first_row_element in second_row:
						# Ustala ze wiersze sie przecinaja
						#print ("przecina sie z", second_row)
						find_overlaping_field (first_row, second_row)
						if purpose == "fork_create":
							#print ("zostalo pole", overlaping_field)
							if overlaping_field != 0 and found == True:
								#print ("Fork zalozony")
								move_par = overlaping_field
								board.move_insertion(player, move_par)
								inserted = True
								ile_forkow += 1
								return True

def find_overlaping_field (first_row, second_row):
	global overlaping_field, found, fork_field_for_blok
	found = False
	#print ("Wspolne dla:", first_row, second_row)
	for temp_overlaping_field in first_row:
		for y in second_row:
			if temp_overlaping_field == y and board.board[temp_overlaping_field] == " ":
				# Finds overlaping field
				#print ("Pole wspolne to:", temp_overlaping_field, "wartosc:", board.board[temp_overlaping_field])
				overlaping_field = temp_overlaping_field
				if overlaping_field not in fork_field_for_blok:
					fork_field_for_blok.append(overlaping_field)
				found = True
	return (overlaping_field)

def computer_move_difficulty_4(player, opponent, game_round):
	# AI with skill to avoid forks
	global inserted, fork_field_for_blok, move_par, ile_blokad_forkow1, ile_blokad_forkow2, temp
	fork_field_for_blok = []
	row_to_block_fork = []
	fork_blok_check = 0
	temp = 0 
	if game_round > 3:
		# print ("Szukam forka")
		find_fork_available_rows(opponent, "fork_block")
		# print ("Pola do forkow:", fork_field_for_blok, "liczba:", len(fork_field_for_blok))
		if len(fork_field_for_blok) == 1:
			# print ("One fork identified - blocking")
			move_par = fork_field_for_blok[0]
			board.move_insertion(player, move_par)
			inserted = True
			ile_blokad_forkow1 += 1
		elif len(fork_field_for_blok) == 2:
			# print ("Two forks identified")
			rows_fork_available = find_fork_available_rows(player, "many_forks")
			# print (rows_fork_available)
			for i in rows_fork_available:
				fork_blok_check = 0
				for j in fork_field_for_blok:
					if j not in i:
						fork_blok_check += 1
				if fork_blok_check == len(fork_field_for_blok):
					row_to_block_fork = i
					break
			# print (row_to_block_fork)
			if len(row_to_block_fork) != 0:
				while True:
					field_to_block_fork = row_to_block_fork[random.randrange(0,3)]
					if board.board[field_to_block_fork] == " ":
						# print ("Wstawiam na:", field_to_block_fork)
						move_par = field_to_block_fork
						board.move_insertion(player, move_par)
						inserted = True
						ile_blokad_forkow2 += 1
						break
			else:
				# nie ma w calosci wolnego rzedu, ktory blokowalby podwojny fork
				pass
	else:
		inserted = False
	if inserted == False:
		general_strategy(player, opponent)

def general_strategy(player, opponent):
	global inserted, move_par
	corner = [1, 3, 7, 9]
	side = [2, 4, 6, 8]
	# Center: You play the center if open
	if board.board[5] == " ":
		move_par = 5
		board.move_insertion(player, move_par)
		inserted = True
		return 0
	# Opposite corner: If the opponent is in the corner, you play the opposite corner.
	if board.last_move == 1 or board.last_move == 3 or board.last_move == 7 or board.last_move == 9:
		if board.board[opposite_corner(board.last_move)] == " ":
			move_par = opposite_corner(board.last_move)
			board.move_insertion(player, move_par)
			inserted = True
			return 0
	# Empty corner: You play in a corner square.
	corner_shuffled = random.sample(corner, 4)
	for i in corner_shuffled:
		if board.board[i] == " ":
			board.move_insertion(player, i)
			inserted = True
			return 0
	# Empty side: You play in a middle square on any of the 4 sides.
	side_shuffled = random.sample(side, 4)
	for i in side_shuffled:
		if board.board[i] == " ":
			move_par = i
			board.move_insertion(player, move_par)
			inserted = True
			return 0

def opposite_corner(opponent_move):
	if opponent_move == 1:
		return 9
	elif opponent_move == 3:
		return 7
	elif opponent_move == 7:
		return 3
	elif opponent_move == 9:
		return 1