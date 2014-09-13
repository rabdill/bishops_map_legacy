# Bishop's Map

A data-driven text adventure engine written in Python. Very much under construction and not particularly usable. All of the things outlined below *do* work, though, and you're welcome to give it a shot.

## Get set up
Just clone the repo into a directory somewhere on your box, and make sure Python is installed – it's been tested with 2.7 but not 3.x.

## Your first room
First, you need to build the room your player is going to start in. "Rooms" are the units that make up the games' maps &ndash; you might start in the "lobby," for example, then `go east` into the "bakery," then `go north` into the woods. Though there are other methods of interacting with the player, every time someone goes somewhere, they're moving from room to room.

Anyway, let's call the first room `lobby`. Go over into main.py and find the line that looks like this, and set the scene name to lobby:
`first_scene="lobby"`

Now we have to make the room itself: Open up rooms.json and add a new room block in between the existing brackets:
```
{
    "lobby": {
    "type" : "room",
    "name" : "the game lobby",
    "exits" : {},
    "entrance text" : {"statement" : "You are in the first room of the new, data-driven world we are creating in an attempt to be a halfway intelligent human."}
}
```

OK, there's a lot going on here:

1. `"lobby" : {`
    - This sets the name of the room, as it's referred to in other places in the system. When you want to say the lobby is to the south of some other room, you would do it using this name. It can be multiple words, if you really want.

2. `"type" : "room",`
    - This sets the item apart from other things, like a `menu` or a `store`.

3. `"name" : "the game lobby",`
    - This is how the room is shown when referenced in the game, to the player. For example, "To the south is the game lobby."

4. `"exits" : {},`
    - This will be a dictionary of other rooms to which the player can `go`. For example, `"exits" : { "east" : "bakery" },` would mean that when the player typed `go east`, they would be taken to the room labeled "bakery." These are printed whenever a player enters a room ("To the east is the muffin bakery.").

5.  `"entrance text" : {"statement" : "You are in the first room of the new, data-driven world we are creating in an attempt to be a halfway intelligent human."}`
    - The entrance text is what is printed when the player is taken to that room. The "statement" delegation is in place because, as you will see later, there can be other items added to the "entrance text" dictionary, such as a `menu`.

That's everything! Your first room is done. Time to take a visit: Just navigate to the directory it's inside of and run `python main.py`, and it should show you the entrance text of your first room!

## Your second room
Let's make another room &ndash call it "bakery," and put it right after the lobby but before the final bracket (and don't forget a comma :
```
{
    "lobby": {
        "type" : "room",
        "name" : "the game lobby",
        "exits" : {},
        "entrance text" : {"statement" : "You are in the first room of the new, data-driven world we are creating in an attempt to be a halfway intelligent human."}
    },

    "bakery": {
        "type" : "room",
        "name" : "the muffin bakery",
        "exits" : {},
        "entrance text" : {"statement" : "This is the bakery!"}
    }
}
```
But now, if you run the program again, you won't be able to move from the lobby to the bakery &ndash; there's nothing indicating that they're connected. Let's say the bakery is to the east of the lobby. First, we have to make the exit in the lobby:
```
    "lobby": {
        "type" : "room",
        "name" : "the game lobby",
        "exits" : {"east" : "bakery"},
        "entrance text" : {"statement" : "You are in the first room of the new, data-driven world we are creating in an attempt to be a halfway intelligent human."}
    },
```
That's it! You just have to say that the room labeled `bakery` is to the east of the `lobby`. If you run the program again, it will display the entrance text of the lobby, plus any valid directions you entered:
```
Bishop's Map v0.1.0

    You are in the first room of the new, data-driven
    world we are creating in an attempt to be a
    halfway intelligent human. 

    To the east is the muffin bakery. 

What do you want to do? > 
```
Now, there's something you *can* do: Just type `go east`:
```
What do you want to do? > go east
    This is the bakery! 

What do you want to do? > 
```
**Huzzah! You moved!**

## About

### The system
Honestly, this whole thing started because I wanted to make a video game for a girl. All I could cobble together at the time was a text game in embarrassingly broken Python, but with a lot of work (and the guidance of several patient friends), I was able to turn thousands of lines of spaghetti code into a system that can parse anybody's game who has the patience to put together the JSON.

Text-based MMORPGs haven't been in vogue for at least a decade. It's been even longer than that in the case of single-player text games, built for a time before graphics cards and computer mice. But interactive fiction done right can still be an amazing experience, and I think any tool that can help facilitate that is a good thing.

### The author
My name is Rich. I'm 24, and I'm still trying to figure out why doing this kind of stuff is so much fun.

### Where the name came from
In 1975, Will Crowther built [*Colossal Cave Adventure*](http://rickadams.org/adventure/a_history.html), planting the seeds for 30 years of text-based gaming with a little game about a magical cavern, based on his real-life caving experiences.

The game was set in a section of Kentucky's [Mammoth Cave](https://en.wikipedia.org/wiki/Mammoth_Cave_National_Park), and, according to legend, the game's cave was rendered faithfully enough that players who went to the real place could find their way around.

One of the first people to find their way around Mammoth Cave, however, was Stephen Bishop, a slave brought to the cave as a guide in 1838. He was the first man to cross the cave's "Bottomless Pit," helping reveal portions of the cave previously unknown. In 1844, he drew a map of the cave, from memory, that was used by explorers for more than 40 years.

Bishop was freed from slavery in 1856, and died of tuberculosis sometime between 1857 and 1859. In 1972, a connection to Mammoth Cave was discovered in the Flint Ridge Cave system, joining it to what is now the longest cave in the world. Revisiting Bishop's map, cavers discovered Bishop had already found and mapped the connection more than a century before.








(misc. notes that don't do anything important yet, but I'll forget:)
A menu with all the options:
    "invasion0" : {
        "type" : "menu",
        "origin" : "town square",
        "prompt" : "T\"Psst,\" you say. \"You OK?\"\n\t\"Yeah,\" she responds. \"My name's Marlo. Do I know you?\"",
        "choices" : [
            "Respond: \"No, I don't suppose you would. I left town a long time ago.\"",
            "Respond: \"No need for the third-degree, I was just checking if you were OK.\"",
            "Respond: \"There's no time for introductions. We have to DO something.\""
        ],

        "responses" : [
            {"loop" : "An excellent choice, this first one. Oh yes.",
                "prompt" : ""},
            {"menu" : "buy cider"},
            {"final" : "You thirded it."}
        ]
    }
    
(write about debug mode)