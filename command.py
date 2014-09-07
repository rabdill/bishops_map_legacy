import printer

def inventory_add(item,qty,player):
    # If the item is already in the player's inventory, give her more, otherwise create the entry:
    if item in player['inventory']:
        player['inventory'][item] += qty
    else:
        player['inventory'][item] = qty

def get(current,rooms,menus,player):
    need_command = True
    
    if current['type'] == "room" and "menu" in current['entrance text']: #if entrance text is a menu label
        menu_name = current['entrance text']['menu'] #save the name so we can clear it from the room
        del(current['entrance text']['menu']) #get rid of the menu so it's only processed once
        current = menus[menu_name] #set the menu as where we are


    if current['type'] == "room":
        while need_command is True:
            #whether the player has been told the results of a command           
            processed_command = False
            
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


            #check if the verb is something that can be done to an item in the room:
            if 'items' in current: #if the room has items
                #if the room has this item:
                if command[1] in current['items']:
                    #if the item can be put into the proposed state:
                    if command[0] in current['items'][command[1]]['states']:
                        #if the item can be put into the proposed state from its current state, do it:
                        if current['items'][command[1]]['status'] in \
                          current['items'][command[1]]['states'][command[0]]['from']:
                            processed_command = True
                            printer.block(current['items'][command[1]]['states'][command[0]]['from'][current['items'][command[1]]['status']])
                            current['items'][command[1]]['status'] = command[0]
                            
                            #special section for "take":
                            if command[0] == 'take':
                                inventory_add(command[1], 1, player)
                                processed_command = True
                        else:
                            printer.block("You can't {0} that item after you {1} it.".format(command[0], current['items'][command[1]]['status']))
                            processed_command = True
                    else:
                        printer.block("Sorry, you can't {} that.".format(command[0]))
                        processed_command = True

            ####
            # "Check actions" block above the generic commands so you can override
            # the generic commands in the actions section.

            if 'actions' in current: #if the room has possible actions
                if command[0] in current['actions']: #if the action is possible
                    #if the noun is a possible recipient of the verb:
                    if command[1] in current['actions'][command[0]]:
                        #if the result is a menu:
                        if "menu" in current['actions'][command[0]][command[1]]:
                            return menus[current['actions'][command[0]][command[1]]["menu"]] 
            
            if command[0] == 'go':
                if command[1] in current['exits']:
                    return rooms[current['exits'][command[1]]]
                else:
                    if processed_command == False:
                        printer.block("That's not a direction in which you can go.")
                        processed_command = True
            elif command[0] == 'look':
                if command[1] in current['exits']:
                    printer.block(rooms[current['exits'][command[1]]]['look'])
                    processed_command = True
                elif command[1] == 'around':
                    return current
                else:
                    if processed_command == False:
                        printer.block("That's not a direction in which you can look.")

            elif command[0] == 'view':
                if command[1] == 'inventory':
                    for item in player['inventory']:
                        printer.block("{0}  x  {1}".format(item, player['inventory'][item]))
                    
                else:
                    if processed_command == False:
                        printer.block("That's not something you can view.")
                
            else:
                if processed_command == False:
                    printer.block("Sorry, unrecognized command.") 
                    processed_command = True


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
                    printer.block("You don't have enough money. That would cost you {} coins.".format(qty * current['items'][command]['price']))

                # Otherwise, buy em:
                else:
                    player['inventory']['coins'] -= qty * current['items'][command]['price']
                    player['inventory'][current['items'][command]['name']] += qty
            
                    printer.block("{0}: You spent {1} coins on {2} of them.".format(current['items'][command]['name'], qty * current['items'][command]['price'], qty))
                    return rooms[current['origin']]

            # If you pick something that isn't an option
            else:
                printer.block("Not an option, friend.")
