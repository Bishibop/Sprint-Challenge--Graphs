from collections import deque
import time
import random
from ast import literal_eval

from room import Room
from player import Player
from world import World

# Load world
world = World()

# You may uncomment the smaller graphs for development and testing purposes.
# map_file = "maps/test_line.txt"
# map_file = "maps/test_cross.txt"
# map_file = "maps/test_loop.txt"
#  map_file = "maps/test_loop_fork.txt"
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

#  Breadth first search method
my_visited = set()
my_visited.add(player.current_room)
bfs_deque = deque()

while len(my_visited) < len(room_graph):
    current_room = player.current_room
    bfs_deque.append((current_room, []))
    nearest_unvisited = None
    bfs_visited = set()
    bfs_visited.add(current_room)
    while not nearest_unvisited:
        room_path = bfs_deque.popleft()
        bfs_visited.add(room_path[0])
        if room_path[0] not in my_visited:
            nearest_unvisited = room_path
            bfs_deque.clear()
        else:
            exits = room_path[0].get_exits()
            rooms = [(room_path[0].get_room_in_direction(exit), exit)
                     for exit in exits]
            unvisited_rooms = [
                room for room in rooms if room[0] not in bfs_visited
            ]
            for room in unvisited_rooms:
                new_path = room_path[1].copy()
                new_path.append(room[1])
                bfs_deque.append((room[0], new_path))
    traversal_path.extend(nearest_unvisited[1])
    for path in nearest_unvisited[1]:
        player.travel(path, show_rooms=False)
    my_visited.add(nearest_unvisited[0])

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
