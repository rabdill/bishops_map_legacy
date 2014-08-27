import json
import printer
import command

json_data = open('rooms.json')

rooms = json.load(json_data)

print "\n\nAbdill Game Engine v0.1.0\n\n"

next_room = "lobby"
    
while True:
    printer.room(next_room,rooms)
    next_room = command.get(next_room,rooms)
