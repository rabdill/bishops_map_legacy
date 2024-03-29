import json
import command
import printer
import sys		#For loading command-line parameters

# Load the game data:
for inFile in ["rooms","menus","player","npc"]:
    json_data = open("{}.json".format(inFile))
    vars()[inFile] = json.load(json_data)

#Check for an automation script:
debug = []
if len(sys.argv) > 1:
	print "DEBUG MODE"
	debug = [line.rstrip('\n') for line in open(sys.argv[1])]

print "\n\nBishop's Map v0.1.0\n\n"

first_scene="lobby"
next_move = rooms[first_scene]
last_move = rooms[first_scene]
printer.scene(next_move,rooms,player,menus,npc,last_move)
next_move = command.get(next_move,rooms,menus,player,npc,debug)

while True:
    printer.scene(next_move,rooms,player,menus,npc,last_move)
    last_move = next_move
    next_move = command.get(next_move,rooms,menus,player,npc,debug)