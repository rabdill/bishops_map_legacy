import textwrap     # for block print

#   Print arbitrary blocks of text:
def block(text):
    if text != "":
        text = text.split('\n')            #split up the text into a list
        print "\t",               #   indents the first line of the block
                                #   THE COMMA PREVENTS A NEWLINE
        for line in text:
            print "\n\t".join( textwrap.wrap(line,50) ),"\n"

# Print all the exits of a room
def directions(location,rooms):
    for direction in location['exits']:
       block("To the {0} is {1}.".format(direction, rooms[location['exits'][direction]]['name']))

def items(items):
    for item in items:
        block(items[item]['states'][items[item]['status']]['descriptor'])



# Process any applicable "change scenarios" in the room:
def process_changes(location,rooms):
    do_change = False
    for condition in location['change scenarios']['conditions']:
        if vars()[condition[0]][condition[1]][condition[2]] == condition[3]:
            do_change = True
        else:
            do_change = False
    if do_change:
        block("CHANGING STUFF")
        for change in location['change scenarios']['changes']:
            vars()[change[0]][change[1]][change[2]] = change[3]
    else:
        block("Business as usual.")

# Go through all the stuff you'd have to print when arriving
# in a new room
def room(location,rooms):
    if "change scenarios" in location:
        process_changes(location,rooms)

    location['visited'] = 1
    block(location['entrance text'])
    if 'items' in location:
        items(location['items'])
    directions(location,rooms)

def menu(menu):
    block(menu["prompt"])
    for choice in menu["choices"]:
        block("{0}: {1}".format(menu["choices"].index(choice), choice))

def store(room,player):
    block(room['greeting'])

    block("FOR SALE:")
    for item in room['items']:
        if item['name'] not in player['inventory']:
            player['inventory'][item['name']] = 0

        print "\t{0}: {1} - {2} coins\n\t\t({3} available)".format(room['items'].index(item), item['name'],item['price'],item['qty available'] )


def scene(current,rooms,player):
    if current['type'] == "room":
        room(current,rooms)
    elif current['type'] == "menu":
        menu(current)
    elif current['type'] == "store":
        store(current,player)
