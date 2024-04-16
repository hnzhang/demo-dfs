def update_energy_and_secrete(rooms, player_info):
	pos_floor, pos_room = player_info[0], player_info[1]
	content = rooms[pos_floor][pos_room]
	energy = player_info[4]
	if content == 'diamond':
		energy += 5
		rooms[pos_floor][pos_room] = 'empty'
	elif content == 'dragon':
		energy -= 5
	elif content == 'secrete':
		player_info[3] = True
		rooms[pos_floor][pos_room] = 'empty'
	# write energy back
	player_info[4] = energy

def move_player(rooms, player_info, command):
	is_inside_room = player_info[2]
	if is_inside_room:
		print("You are in a room, and you have exit first to move in the hallway")
		return
	MAX_ROOM = len(rooms[0])
	MAX_FLOOR = len(rooms)
	
	pos_floor, pos_room = player_info[0], player_info[1]
	if command == 'A'  and pos_room > 0:
			pos_room -= 1
	elif command == 'D' and pos_room < MAX_ROOM - 1:
		pos_room += 1
	elif command == 'W' and (pos_room == 0 or pos_room == MAX_ROOM -1) and pos_floor < MAX_FLOOR -1 and player_info[4] > 3:
		pos_floor += 1
		player_info[4] -= 3 # consume 3 pt per climbing
	elif command == 'S' and (pos_room == 0 or pos_room == MAX_ROOM -1) and pos_floor > 0:
		pos_floor -= 1
	else:
		print("invalid moving command: ", command)
	player_info[0], player_info[1] = pos_floor, pos_room

def update_player(rooms, player_info, command):
	''' if the player is at the very left of  each floor, the player cannot move to the left
			if the player is at the very right of each floor, the player cannot move to the right
			
			the player can move up or down only when the player is the end of each floor because
			the stairs are at the end of the building

			if the player is inside a room, the player cannot move left or right in the hallway.
	'''
	pos_floor, pos_room = player_info[0], player_info[1]
	command = command.upper()
	is_inside_room = player_info[2]
	if command == 'E':
		if not is_inside_room:
			is_inside_room = True
			print("entering the room ", pos_floor, pos_room)
			update_energy_and_secrete(rooms, player_info)
		else:
			print("exiting the room ", pos_floor, pos_room)
			is_inside_room = False
		# write info back
		player_info[2] = is_inside_room
	elif command == 'B':
		if player_info[3] == True and pos_floor == 3 and pos_room == 0:
			print("You are boarding the Helicopter! Great Job!")
			player_info[5] = True
		else:
			print("You cannot board the Helicopter. You have to be in the room(3,0) with the secrete")
	elif command == 'W' or command == 'A' or command == 'S' or command == 'D':
		move_player(rooms, player_info, command)
	else:
		print("Unrecognizable command:", command, "skipped!")

def display_player_info(player_info):
	print("== player info ==")
	print("  Position: Floor: ", player_info[0], " Room: ",player_info[1], end = "")
	print(" | ✨. ", player_info[4], " | Secrete:", "✅" if player_info[3] else "❌" , end = '')
	is_inside_room = player_info[2]
	print(" | Inside Room? ", "Yes" if is_inside_room else "No")

def take_user_input():
	user_input = input("choose action: move [w, a, s, d] (E)nter/(E)xit, (B)oard, (Q)uit ]: ")
	user_input = user_input.upper()
	return user_input