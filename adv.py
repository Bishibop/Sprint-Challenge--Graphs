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
map_file = "maps/main_maze.txt"

# Loads the map into a dictionary
room_graph = literal_eval(open(map_file, "r").read())
world.load_graph(room_graph)

# Print an ASCII map
world.print_rooms()

player = Player(world.starting_room)

# Fill this out with directions to walk
# traversal_path = ['n', 'n']
traversal_path = []

print('my algo')
first_entered = {}
first_entered[player.current_room] = None
direction_swap = {'n': 's', 's': 'n', 'e': 'w', 'w': 'e'}
#  backtrack1 = deque()
#  backtrack2 = []

while len(first_entered) < len(room_graph):
    current_room = player.current_room
    #  print('cur: ', current_room.id, end=', ')
    #  print('total: ', len(first_entered))
    #  time.sleep(1)
    exits = current_room.get_exits()
    rooms = [(current_room.get_room_in_direction(exit), exit)
             for exit in exits]
    next_room = next((room for room in rooms if room[0] not in first_entered),
                     None)
    if next_room:
        #  print('next room: ', next_room)
        #  if backtrack2:
        #      traversal_path.extend(backtrack1)
        #      traversal_path.extend(backtrack2)
        #      backtrack1.clear()
        #      backtrack2.clear()
        first_entered[next_room[0]] = direction_swap[next_room[1]]
        traversal_path.append(next_room[1])
        player.travel(next_room[1], show_rooms=False)
    else:
        #  print('backtracking...')
        backwards = first_entered[current_room]
        traversal_path.append(backwards)
        player.travel(backwards, show_rooms=False)

# TRAVERSAL TEST - DO NOT MODIFY
visited_rooms = set()
player.current_room = world.starting_room
visited_rooms.add(player.current_room)

for move in traversal_path:
    player.travel(move)
    visited_rooms.add(player.current_room)

if len(visited_rooms) == len(room_graph):
    print(
        f"TESTS PASSED: {len(traversal_path)} moves, {len(visited_rooms)} rooms visited"
    )
else:
    print("TESTS FAILED: INCOMPLETE TRAVERSAL")
    print(f"{len(room_graph) - len(visited_rooms)} unvisited rooms")

#######
# UNCOMMENT TO WALK AROUND
#######
#  player.current_room.print_room_description(player)
#  while True:
#      cmds = input("-> ").lower().split(" ")
#      if cmds[0] in ["n", "s", "e", "w"]:
#          player.travel(cmds[0], True)
#      elif cmds[0] == "q":
#          break
#      else:
#          print("I did not understand that command.")
