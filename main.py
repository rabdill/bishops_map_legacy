import json
import command
import printer

json_data = open('rooms.json')
rooms = json.load(json_data)

json_data = open('menus.json')
menus = json.load(json_data)

print "\n\nBishop's Map v0.1.0\n\n"

current = rooms["lobby"]
printer.room(current,rooms)

next_move = command.get(current,rooms,menus)

while True:
    if next_move['type'] == "room":
        printer.room(next_move,rooms)
    elif next_move['type'] == "menu":
        printer.menu(next_move)
    current = next_move

    next_move = command.get(current,rooms,menus)
