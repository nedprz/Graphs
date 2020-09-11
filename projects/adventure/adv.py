from room import Room
from player import Player
from world import World

import random
from ast import literal_eval

# Load world
world = World()


# You may uncomment the smaller graphs for development and testing purposes.
# map_file = "maps/test_line.txt"
# map_file = "maps/test_cross.txt"
# map_file = "maps/test_loop.txt"
# map_file = "maps/test_loop_fork.txt"
map_file = "projects/adventure/maps/main_maze.txt"

# Loads the map into a dictionary
room_graph=literal_eval(open(map_file, "r").read())
world.load_graph(room_graph)

# Print an ASCII map
world.print_rooms()

player = Player(world.starting_room)

# Fill this out with directions to walk
# traversal_path = ['n', 'n']
traversal_path = []
################################################


# we will call visited a set so we don't double count rooms


visited = set()  


#define variables to be used for directions of walk
prev = ''
next = ''
landlocked = dict()

player.current_room = world.starting_room
visited.add(player.current_room.id)

#We will walk south to start
direction = 's'
traversal_path.append(direction)

#define number of rooms and loop through until they are all visited
ROOMS = 500
while len(visited) < ROOMS:
    player.travel(direction)
    visited.add(player.current_room.id)

    prev = direction

    # Traversal process 

    if prev == 's':
        if 'w' in player.current_room.get_exits():
            direction = 'w'
        elif 's' in player.current_room.get_exits():
            direction = 's'
        elif 'e' in player.current_room.get_exits():
            direction = 'e'
        else: 
            direction = 'n'
    
    elif prev == 'n':
        if 'e' in player.current_room.get_exits():
            direction = 'e'
        elif 'n' in player.current_room.get_exits():
            direction = 'n'
        elif 'w' in player.current_room.get_exits():
            direction = 'w'
        else: 
            direction = 's'
    
    elif prev == 'w':
        if 'n' in player.current_room.get_exits():
            direction = 'n'
        elif 'w' in player.current_room.get_exits():
            direction = 'w'
        elif 's' in player.current_room.get_exits():
            direction = 's'
        else: 
            direction = 'e'

    elif prev == 'e':
        if 's' in player.current_room.get_exits():
            direction = 's'
        elif 'e' in player.current_room.get_exits():
            direction = 'e'
        elif 'n' in player.current_room.get_exits():
            direction = 'n'
        else: 
            direction = 'w'
    

    # Takes care of special case where a room is "landlocked" by 4 other rooms, which can lead to an infinite loop 
    if len(player.current_room.get_exits()) == 4:
        current = player.current_room.id

        if current not in landlocked:
            landlocked[current] = []
        
        if direction not in landlocked[current]:
            landlocked[current].append(direction)
        
        elif len(landlocked[current]) < 4:
            direction = random.choice([i for i in ['n', 's', 'e', 'w'] if i not in landlocked[current]])
            landlocked[current].append(direction)
        
        else:
            direction = landlocked[current][len(landlocked[current])%4] 
            landlocked[current].append(direction)

    # Add the next movement to the traversal_path
    traversal_path.append(direction)


# TRAVERSAL TEST
visited_rooms = set()
player.current_room = world.starting_room
visited_rooms.add(player.current_room)

for move in traversal_path:
    player.travel(move)
    visited_rooms.add(player.current_room)

if len(visited_rooms) == len(room_graph):
    print(f"TESTS PASSED: {len(traversal_path)} moves, {len(visited_rooms)} rooms visited")
else:
    print("TESTS FAILED: INCOMPLETE TRAVERSAL")
    print(f"{len(room_graph) - len(visited_rooms)} unvisited rooms")

#######
# UNCOMMENT TO WALK AROUND
#######
#player.current_room.print_room_description(player)
#while True:
#    cmds = input("-> ").lower().split(" ")
#    if cmds[0] in ["n", "s", "e", "w"]:
#        player.travel(cmds[0], True)
#    elif cmds[0] == "q":
#        break
#    else:
#        print("I did not understand that command.")
