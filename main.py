import json
import command
import printer

for inFile in ["rooms","menus","player"]:
    json_data = open("{}.json".format(inFile))
    vars()[inFile] = json.load(json_data)

print "\n\nBishop's Map v0.1.0\n\n"

first_scene="drury lane"

printer.scene(rooms[first_scene],rooms,player)
next_move = command.get(rooms[first_scene],rooms,menus,player)

while True:
    printer.scene(next_move,rooms,player)
    next_move = command.get(next_move,rooms,menus,player)
