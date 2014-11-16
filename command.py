import printer


def get_text(prompt,debug, player):
    if len(debug) == 0:
        return raw_input(prompt)
    else:
        result = debug.pop(0)
        printer.block("{0}FILE: {1}".format(prompt,result), player)
        return result


def inventory_add(item,qty,player):
    # If the item is already in the player's inventory, give her more, otherwise create the entry:
    if item in player['inventory']:
        player['inventory'][item] += qty
    else:
        player['inventory'][item] = qty

def get(current,rooms,menus,player,npc,debug):
    need_command = True
    
    #if it's a room that presents a menu upon entering:
    if current['type'] == "room" and "menu" in current['entrance text']: #if entrance text is a menu label
        menu_name = current['entrance text']['menu'] #save the name so we can clear it from the room
        del(current['entrance text']['menu']) #get rid of the menu so it's only processed once
        current = menus[menu_name] #set the menu as where we are


    if current['type'] == "room":
        while need_command is True:
            #whether the player has been told the results of a command           
            processed_command = False
            
            command = get_text("What do you want to do? > ", debug, player).split() # makes the command a list

            # Strip out the articles:
            #*Make this less ugly
            articles = ["the", "to", "a", "an", "in", "out"]
            for article in articles:
                i = 0
                while i < len(command): 
                    if command[i] == article:
                        command.pop(i)
                    i += 1
            #check to see if the direct object is 2 words instead of 1:
            if len(command) > 2:
                command[1] += " " + command[2]
                #*add a line here to delete what used to be command[2]
            
            #check if it isn't long enough:
            if len(command) < 2:
               printer.block("Sorry, command too short.", player)
               processed_command = True
            else:
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
                            elif "statement" in current['actions'][command[0]][command[1]]:
                                printer.block(current['actions'][command[0]][command[1]]["statement"], player)
                                processed_command = True

                #check if the verb is something that can be done to an item in the room:
                #**add "continue" statements here instead of nested ifs***
                if 'items' in current and processed_command == False: #if the room has items
                    #if the room has this item:
                    if command[1] in current['items']:
                        #if the item can be put into the proposed state:
                        if command[0] in current['items'][command[1]]['states']:
                            #if the item can be put into the proposed state from its current state, do it:
                            if current['items'][command[1]]['status'] in \
                              current['items'][command[1]]['states'][command[0]]['from']:
                                processed_command = True
                                printer.block(current['items'][command[1]]['states'][command[0]]['from'][current['items'][command[1]]['status']], player)
                                current['items'][command[1]]['status'] = command[0]
                                
                                #special section for "take":
                                if command[0] == 'take':
                                    inventory_add(current['items'][command[1]]["name"], 1, player)
                                    processed_command = True

                                #if acting on the object changes other things:
                                if "changes" in current['items'][command[1]]['states'][command[0]]:
                                    printer.process_changes(current['items'][command[1]]['states'][command[0]]['changes'],rooms,menus,player,npc)

                            else:
                                printer.block("You can't {0} that item after you {1} it.".format(command[0], current['items'][command[1]]['status']), player)
                                processed_command = True
                        else:
                            #If there is a specific message to tell the user the action can't be done:
                            if "disallowed states" in current['items'][command[1]] and command[0] in current['items'][command[1]]['disallowed states']:
                                printer.block(current['items'][command[1]]['disallowed states'][command[0]], player)
                                processed_command = True
                            elif command[0] == "inspect":
                                printer.block("Nothing spectacular about it.", player)
                                processed_command = True
                            else:
                                printer.block("Sorry, you can't {} that.".format(command[0]), player)
                                processed_command = True
                if command[0] == 'go':
                    if command[1] in current['exits']:
                        return rooms[current['exits'][command[1]]]
                    else:
                        if processed_command == False:
                            printer.block("That's not a direction in which you can go.", player)
                            processed_command = True
                elif command[0] == 'look':
                    if command[1] in current['exits'] and processed_command is False:
                        printer.block(rooms[current['exits'][command[1]]]['look'], player)
                        processed_command = True
                    elif command[1] == 'around':
                        return current
                    else:
                        if processed_command == False:
                            printer.block("That's not a direction in which you can look.", player)

                elif command[0] == 'view':
                    if command[1] == 'inventory':
                        for item in player['inventory']:
                            if player['inventory'][item] > 0:
                                printer.block("{0}  x  {1}".format(item, player['inventory'][item]), player)
                        
                    else:
                        if processed_command == False:
                            printer.block("That's not something you can view.", player)
                    
                else:
                    if processed_command == False:
                        printer.block("Sorry, unrecognized command.", player)
                        processed_command = True


    elif current['type'] == "menu":
        while True:
            choice = get_text("Which do you choose? > ", debug, player)
            try:
                command = int(choice)
            except ValueError:  #if it's not an integer
                command = len( current['choices']) #skips all the checking and asks for another response

            if command < len( current['choices']):
                #if you want to print a message before the next printing
                if "premessage" in current['responses'][command]:
                    printer.block(current['responses'][command]["premessage"], player)
                #NOTE: The ONLY thing that happens before the changes listed in a
                #response is the premessage. Everything else happens afterward.
                #if any variables get shifted around
                if "changes" in current['responses'][command]:
                    printer.process_changes(current['responses'][command]['changes'],rooms,menus,player,npc)

                # if it just says something, then returns you to the room:
                if "final" in current['responses'][command]:
                    printer.block(current['responses'][command]["final"], player)
                    return rooms[current['origin']]
                
                #if you should get the same menu again
                elif "loop" in current['responses'][command]:
                    printer.block(current['responses'][command]["loop"], player)
                    
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
                printer.block("Not an option, bub.", player)


    elif current['type'] == "store":
        while True:
            command = int(get_text("Which item to buy? > ", debug, player))
            if command < len(current['items']):
                qty = int(get_text("How many? (You have {0} coins, or enough for as many as {1}) > ".format(player['inventory']['coins'], player['inventory']['coins']/current['items'][command]['price'] ), debug, player))
                # If you want to buy more than the store has:
                if qty > current['items'][command]['qty available']:
                    block("The store doesn't have that many available.")
            
                # If you can't afford that many:
                elif (qty * current['items'][command]['price']) > player['inventory']['coins']:
                    printer.block("You don't have enough money. That would cost you {} coins.".format(qty * current['items'][command]['price']), player)

                # Otherwise, buy em:
                else:
                    if qty > 0:
                        inventory_add('coins', -1 * qty * current['items'][command]['price'], player)
                        inventory_add(current['items'][command]['name'], qty, player)
                
                        printer.block("{0}: You spent {1} coins on {2} of them.".format(current['items'][command]['name'], qty * current['items'][command]['price'], qty), player)
                    return rooms[current['origin']]

            # If you pick something that isn't an option
            else:
                printer.block("Not an option, friend.", player)