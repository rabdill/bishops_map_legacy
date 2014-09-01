import printer

def inventory_add(item,qty,player):
    if item in player['inventory']:
        player['inventory'][item] += qty
    else:
        player['inventory'][item] = qty

def get(current,rooms,menus,player):
    need_command = True
    if current['type'] == "room":
        while need_command is True:
            command = raw_input("What do you want to do? > ").split() # makes it a list
            # Strip out the articles:
            try:
                command.remove("the")
            except Exception: 
                pass
            try:
                command.remove("to")
            except Exception: 
                pass
            try:
                command.remove("a")
            except Exception: 
                pass
            try:
                command.remove("an")
            except Exception: 
                pass
            try:
                command.remove("in")
            except Exception: 
                pass  

            # if the verb is a possible action:
            if 'actions' in current:
                if command[0] in current['actions']:
                    #if the noun is a possible recipient of the verb:
                    if command[1] in current['actions'][command[0]]:
                        #if the result is a menu:
                        if "menu" in current['actions'][command[0]][command[1]]:
                            return menus[current['actions'][command[0]][command[1]]["menu"]]   

            if command[0] == 'go':
                if command[1] in current['exits']:
                    return rooms[current['exits'][command[1]]]
                else:
                    printer.block("That's not a direction in which you can go.") 

            elif command[0] == 'look':
                if command[1] in current['exits']:
                    printer.block(rooms[current['exits'][command[1]]]['look'])
                else:
                    printer.block("That's not a direction in which you can look.")

            elif command[0] == 'view':
                if command[1] == 'inventory':
                    for item in player['inventory']:
                        printer.block("{0}  x  {1}".format(item, player['inventory'][item]))
                    
                else:
                    printer.block("That's not something you can view.")
                
            elif command[0] == 'take':
                if 'items' in current:    # if there are items
                    if command[1] in current['items']: #if the specified item exists
                        if 'take' in current['items'][command[1]]['states']: #if it can be taken
                            inventory_add(command[1], 1, player)
                            if current['items'][command[1]]['states'][command[0]] == "":
                                del current['items'][command[1]] #delete it
                            else:
                                current['items'][command[1]]['status'] = command[0]
                            printer.block("You took it.")
                        else:
                            block("You can't take that item.")
                    else:
                        block("That's not a recognized item here.")
                else:
                    printer.block("There is nothing to take.")
            else:
                printer.block("Sorry, unrecognized command.")


    elif current['type'] == "menu":
        while True:
            command = int(raw_input("Which do you choose? > "))
            if command < len( current['choices']):
                # if it just says something, then returns you to the room:
                if "final" in current['responses'][command]:
                    printer.block(current['responses'][command]["final"])
                    return rooms[current['origin']]
                
                #if you should get the same menu again
                elif "loop" in current['responses'][command]:
                    printer.block(current['responses'][command]["loop"])
                    
                    # If the loop changes the menu's prompt:
                    if current['responses'][command]["prompt"] != "":
                        current["prompt"] = current['responses'][command]["prompt"]
                    return current
                
                # If it's another menu, send the next menu along:
                elif "menu" in current['responses'][command]:
                    return menus[current['responses'][command]["menu"]]

                elif "room" in current['responses'][command]:
                    return rooms[current['responses'][command]["room"]]
            else:
                printer.block("Not an option, bub.")


    elif current['type'] == "store":
        while True:
            command = int(raw_input("Which item to buy? > "))
            if command < len(current['items']):
                qty = int(raw_input("How many? (You have {0} coins, or enough for as many as {1}) > ".format(player['inventory']['coins'], player['inventory']['coins']/current['items'][command]['price'] )))
                # If you want to buy too many:
                if qty > current['items'][command]['qty available']:
                    block("The store doesn't have that many available.")
            
                # If you can't afford that many:
                elif (qty * current['items'][command]['price']) > player['inventory']['coins']:
                    block("You don't have enough money. That would cost you {} coins.".format(qty * current['items'][command]['price']))

                # Otherwise, buy em:
                else:
                    player['inventory']['coins'] -= qty * current['items'][command]['price']
                    player['inventory'][current['items'][command]['name']] += qty
            
                    printer.block("{0}: You spent {1} coins on {2} of them.".format(current['items'][command]['name'], qty * current['items'][command]['price'], qty))
                    return rooms[current['origin']]

            # If you pick something that isn't an option
            else:
                printer.block("Not an option, friend.")
