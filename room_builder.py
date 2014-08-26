import json

def build_rooms():
    rooms = {}

    lobby={
        "name" : "the game lobby",
        "entrance_text" : "You are in the first room of the new, data-driven \
            world we are creating in an attempt to be a halfway intelligent human.",
        "exits" : {
            "south" : "config_room",
            "west"  : "bathroom"
        }
    }

    rooms['lobby']=lobby

    bathroom={
        "name" : "the bathroom",
        "entrance_text" : "You're in the crapper.",
        "exits" : {
            "east" : "lobby"
            }
    }

    rooms['bathroom']=bathroom
    
    config_room={
        "name" : "the configuration zone",
        "entrance_text" : "Sup? This is where we'll get player data.",
        "exits" : {
            "north" : "lobby"
            }
    }

    rooms['config_room']=config_room

    #jsonfile = open('rooms.json','w')
    #json.dump(rooms,jsonfile)
    #jsonfile.close()


    return rooms