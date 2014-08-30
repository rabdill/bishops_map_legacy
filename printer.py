import textwrap     # for block print

#   Print arbitrary blocks of text:
def block(text):
    text = text.split('\n')            #split up the text into a list
    print "\t",               #   indents the first line of the block
                                #   THE COMMA PREVENTS A NEWLINE
    for line in text:
        print "\n\t".join( textwrap.wrap(line,50) ),"\n"

# Print all the exits of a room
def directions(location,rooms):
    for direction in location['exits']:
       block("To the {0} is {1}.".format(direction, rooms[location['exits'][direction]]['name']))


# Go through all the stuff you'd have to print when arriving
# in a new room
def room(location,rooms):
    block(location['entrance_text'])
    directions(location,rooms)

def menu(menu):
    block(menu["prompt"])
    for choice in menu["choices"]:
        block("{0}: {1}".format(choice,menu["choices"][choice]))

def store(room):
    block(room['greeting'])
    block("For sale:")
    for item in room['items']:  #the "items()" is a built-in python method
        for key,value in item.iteritems():
            block("{0}: ${1}".format(key,value))

def scene(current,rooms):
    if current['type'] == "room":
        room(current,rooms)
    elif current['type'] == "menu":
        menu(current)
    elif current['type'] == "store":
        store(current)
