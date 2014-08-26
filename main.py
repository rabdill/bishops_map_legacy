import json
import printer

json_data = open('rooms.json')

rooms = json.load(json_data)

print "\n\nAbdill Game Engine v0.1.0\n\n"

next_room = "lobby"
    
while True:
    printer.room(next_room,rooms)
    need_answer = True

    while need_answer is True:
        direction = raw_input("Which direction do you want to go? ")
        if direction not in rooms[next_room]['exits']:
            printer.block("That's not a direction in which you can go.")
        else:
            need_answer = False

    next_room = rooms[next_room]['exits'][direction]
