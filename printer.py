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



# Process any applicable "change scenarios" in a room:
def check_for_changes(location,rooms,player,menus,npc):
    for scenario in location['change scenarios']: #go through each scenario set
        do_change = 0 #the number of conditions that were actually met
        for condition in scenario['conditions']: #check all the conditions
            if len(condition) == 2: #needs to be at least 2: a variable and a criteria
                if vars()[condition[0]] == condition[1]:
                    do_change += 1
            elif len(condition) == 3:  #if the variable in question is nested 1 level in
                if vars()[condition[0]][condition[1]] == condition[2]:
                    do_change += 1
            elif len(condition) == 4: #if the variable is nested 2 levels in
                if vars()[condition[0]][condition[1]][condition[2]] == condition[3]:
                    do_change += 1
            elif len(condition) == 5: # 3 levels in, etc, etc
                if vars()[condition[0]][condition[1]][condition[2]][condition[3]] == condition[4]:
                    do_change += 1
            elif len(condition) == 6:
                if vars()[condition[0]][condition[1]][condition[2]][condition[3]][condition[4]] == condition[5]:
                    do_change += 1
            elif len(condition) == 7:
                if vars()[condition[0]][condition[1]][condition[2]][condition[3]][condition[4]][condition[5]] == condition[6]:
                    do_change += 1

        if do_change == len(scenario['conditions']): #if all the criteria are satisfied
            process_changes(scenario['changes'],rooms,menus,player,npc)

def process_changes(changes,rooms,menus,player,npc):
    for change in changes:
        # if it's a health modifier:
        if "health" in change:
            #if it's the player's health:
            if "player" in change:
                player["health"] += change[2]
                if change[2] > 0:
                    block("You gain {0} health points! (Now at {1}.)".format(change[2],player["health"])) 
                else:
                    block("You lose {0} health points! (Now at {1}.)".format(-change[2],player["health"]))
            #if it's an NPC:
            else:
                npc[change[1]]["health"] += change[3]
                if change[3] > 0:
                    block("{0} gains {1} health points! (Now at {2}.)".format(npc[change[1]]["name"],change[3],npc[change[1]]["health"]))
                else:
                    block("{0} loses {1} health points! (Now at {2}.)".format(npc[change[1]]["name"],change[3],npc[change[1]]["health"]))
        #if it's any other modifier:
        else:
            if len(change) == 2:
                vars()[change[0]] = change[1]
            elif len(change) == 3:
                vars()[change[0]][change[1]] = change[2]
            elif len(change) == 4:
                vars()[change[0]][change[1]][change[2]] = change[3]
            elif len(change) == 5:
                vars()[change[0]][change[1]][change[2]][change[3]] = change[4]
            elif len(change) == 6:
                vars()[change[0]][change[1]][change[2]][change[3]][change[4]] = change[5]
            elif len(change) == 7:
                vars()[change[0]][change[1]][change[2]][change[3]][change[4]][change[5]] = change[6]

# Go through all the stuff you'd have to print when arriving
# in a new room
def room(location,rooms,menus,player,npc):
    if "change scenarios" in location:
        check_for_changes(location,rooms,player,menus,npc)

    location['visited'] = 1
    
    if "menu" in location['entrance text']: #if there's a menu, it takes precedence over everything else
        menu(menus[location['entrance text']['menu']])
    elif "statement" in location['entrance text']:
        block(location['entrance text']['statement'])
        if 'items' in location:
            items(location['items'])
        directions(location,rooms)

def menu(menu,rooms,menus,player,npc):
    block(menu["prompt"])
    print "\t\t\t\t--"
    for choice in menu["choices"]:
        block("{0}: {1}".format(menu["choices"].index(choice), choice))
    if "changes" in menu:
        process_changes(menu['changes'],rooms,menus,player,npc)

def store(room,player):
    block(room['greeting'])

    block("FOR SALE:")
    for item in room['items']:
        if item['name'] not in player['inventory']:
            player['inventory'][item['name']] = 0

        print "\t{0}: {1} - {2} coins\n\t\t({3} available)".format(room['items'].index(item), item['name'],item['price'],item['qty available'] )


def scene(current,rooms,player,menus,npc):
    if current['type'] == "room":
        room(current,rooms,menus,player,npc)
    elif current['type'] == "menu":
        menu(current,rooms,menus,player,npc)
    elif current['type'] == "store":
        store(current,player)
