def check_winners(winner):
	winner_total[winner] = winner_total.get(winner, "0") + 1

def check_game_rounds(game_round):
	game_round_count_total[game_round] = game_round_count_total.get(game_round, "0") + 1
	return 0

def check_game_times(single_game_time, game_round):
	global game_time_total, game_time_average
	game_time_total += single_game_time
	game_time_average = game_time_total / game_count_total
	game_round_time_total[game_round] = game_round_time_total.get(game_round, "0") + single_game_time

def check_field_frequency_abs(winning_combination):
	global total_wins_count
	for field in winning_combination:
		field_frequency_abs[int(field)] = field_frequency_abs.get(int(field), "0") + 1
	total_wins_count = winner_total["O"] + winner_total["X"]
	for i in (range(1,10)):
		if field_frequency_abs.get(int(i)) > 0:
			field_frequency_per[i] = (field_frequency_abs.get(int(i), "0"))/(total_wins_count)

def print_results():
	print (str(game_count_total).center(20, "*"))
	print ()
	print ("WINNERS".center(20, "-"))
	print ("O".ljust(10,"."), str((winner_total.get("O", "0"))).rjust(10,"."), sep="")
	print ("X".ljust(10,"."), str((winner_total.get("X", "0"))).rjust(10,"."), sep="")
	print ("Draw".ljust(10,"."), str((winner_total.get("D", "0"))).rjust(10,"."), sep="")
	print ()
	print ("ROUNDS".center(20, "-"))
	for i in (range(1,10)):
		if game_round_count_total.get(int(i)) > 0:
			print (str(i).ljust(10,"."), str((game_round_count_total.get(int(i), "0"))).rjust(10,"."), sep="")
	print ()
	print ("TIME".center(20, "-"))
	print ("Total".ljust(10,"."), (str(game_time_total))[0:10].rjust(10,"."), sep="")
	print ("Average".ljust(10,"."), (str(game_time_average))[0:10].rjust(10,"."), sep="")
	for i in (range(1,10)):
		if game_round_count_total.get(int(i)) > 0:
			print (str(i).ljust(10,"."), str((game_round_time_total.get(int(i), "0"))/(game_round_count_total.get(int(i), "0")))[0:10].rjust(10,"."), sep="")
	print ()
	print ("FIELD FREQUENCY".center(20, "-"))
	for i in (range(1,10)):
		if field_frequency_abs.get(int(i)) > 0:
			print (str(i).ljust(10,"."), (str(round(field_frequency_per[i]*100,1))+"%").rjust(10,"."), sep="")

file_path = "wyniki.txt"
file = open (file_path, "r")
winner_total = {"O":0, "X": 0, "D":0}
game_round_count_total = {1:0, 2:0, 3:0, 4:0, 5:0, 6:0, 7:0, 8:0, 9:0}
game_round_time_total = {1:0, 2:0, 3:0, 4:0, 5:0, 6:0, 7:0, 8:0, 9:0}
field_frequency_abs = {1:0, 2:0, 3:0, 4:0, 5:0, 6:0, 7:0, 8:0, 9:0}
field_frequency_per = {1:0, 2:0, 3:0, 4:0, 5:0, 6:0, 7:0, 8:0, 9:0}
game_time_total = 0
game_time_average = 0
game_count_total = 0
for i in file.readlines():
	game_count_total += 1
	line = i[0:-1]
	line = line.split(":")
	check_winners (line[0])
	check_game_rounds (int(line[1]))
	check_game_times (float(line[2]), int(line[1]))
	check_field_frequency_abs (line[4])
print_results()

