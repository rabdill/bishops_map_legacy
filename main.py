import json
import printer
import command

json_data = open('rooms.json')

rooms = json.load(json_data)

print "\n\nAbdill Game Engine v0.1.0\n\n"

current_room = "lobby"
printer.room(current_room,rooms)

while True:
    next_move = command.get(current_room,rooms)

    if rooms[next_move]['type'] == 'room':
        printer.room(next_move,rooms)
        current_room = next_move  
