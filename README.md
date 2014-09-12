bishops_map
===========

A data-driven text adventure engine written in Python. Very much under construction and not usable yet.

The .py files are the game engine, the .json files contain a generic game being used for testing. JSON can be replaced with anything your little heart desires.


"change scenarios" : [
        {
            "conditions" : [
                ["rooms", "drury lane front", "visited", 1],
                ["player", "inventory", "coins", 100]
            ],
            "changes" : [
                ["rooms", "town square", "entrance text", {"statement" : "COIN ONE! HUZZAH!"} ]
            ]

        },

        {
            "conditions" : [
                ["rooms", "cider brewery", "visited", 1],
                ["rooms", "parents house", "visited", 1]
            ],
            "changes" : [
                ["rooms", "town square", "entrance text", {"menu" : "invasion0",
                    "statement" : "Everyone is hiding after the invasion."} ]
            ]
        }
    ],