import printer

def get(current,rooms,menus):
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
            if command[0] in current['actions']:
                #if the noun is a possible recipient of the verb:
                if command[1] in current['actions'][command[0]]:
                    #if the result is a menu:
                    if "menu" in current['actions'][command[0]][command[1]]:
                        return menus[current['actions'][command[0]][command[1]]["menu"]]   

            elif command[0] == 'go':
                if command[1] not in current['exits']:
                    printer.block("That's not a direction in which you can go.") 
                else:
                    need_command = False
                    return rooms[current['exits'][command[1]]]

            elif command[0] == 'look':
                if command[1] not in current['exits']:
                    printer.block("That's not a direction in which you can look.")
                else:
                    printer.block(rooms[current['exits'][command[1]]]['look'])
            else:
                printer.block("Sorry, unrecognized command.")


    elif current['type'] == "menu":
        while True:
            command = raw_input("Which do you choose? > ")
            if command in current['choices']:
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
