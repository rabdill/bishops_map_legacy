# Bishop's Map

A data-driven text adventure engine written in Python. Very much under construction and not particularly usable. All of the things outlined below *do* work, though, and you're welcome to give it a shot.

Markdown isn't the perfect formatting syntax for JSON, so if you get lost with weird indents, just check out some of the project's JSON files for reference.

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

## About

### The system
Honestly, this whole thing started because I wanted to make a video game for a girl. All I could cobble together at the time was a text game in embarrassingly broken Python, but with a lot of work (and the guidance of several patient friends), I was able to turn thousands of lines of spaghetti code into a system that can parse anybody's game who has the patience to put together the JSON.

Text-based MMORPGs haven't been in vogue for at least a decade. It's been even longer than that in the case of single-player text games, built for a time before graphics cards and computer mice. But interactive fiction done right can still be an amazing experience, and I think any tool that can help facilitate that is a good thing.

### The author
My name is Rich. I'm 24, and I'm still trying to figure out why doing this kind of stuff is so much fun.

## Where the name came from
In 1975, Will Crowther built [*Colossal Cave Adventure*](http://rickadams.org/adventure/a_history.html), planting the seeds for 30 years of text-based gaming with a little game about a magical cavern, based on his real-life caving experiences.

The game was set in a section of Kentucky's [Mammoth Cave](https://en.wikipedia.org/wiki/Mammoth_Cave_National_Park), and, according to legend, the game's cave was rendered faithfully enough that players who went to the real cave could find their way around.

One of the first people to find their way around Mammoth Cave, however, was Stephen Bishop, a slave brought to the cave as a guide in 1838. He was the first man to cross the cave's "Bottomless Pit," helping reveal portions of the cave previously unknown. In 1844, he drew a map of the cave, from memory, that was used by explorers for more than 40 years.

Bishop was freed from slavery in 1856, and died of tuberculosis sometime between 1857 and 1859. In 1972, a connection to Mammoth Cave was discovered in the Flint Ridge Cave system, joining it to what is now the longest cave in the world. Revisiting Bishop's map, cavers discovered Bishop had already found and mapped the connection more than a century before.