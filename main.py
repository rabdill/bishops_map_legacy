import json
import command
import printer

for inFile in ["rooms","menus"]:
    json_data = open("{}.json".format(inFile))
    vars()[inFile] = json.load(json_data)

print "\n\nBishop's Map v0.1.0\n\n"

next_move = rooms["lobby"]

while True:
    if next_move['type'] == "room":
        printer.room(next_move,rooms)
    elif next_move['type'] == "menu":
        printer.menu(next_move)
    next_move = command.get(next_move,rooms,menus)
