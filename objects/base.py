"""
This file should contain only the "base" class for blocks/tools/players/mobs

Essentially, they're abstract base classes. Put example objects in "default.py".

This is so that mods can remove default objects from their game.
"""

from collections import defaultdict

uids = defaultdict(lambda: None)


class Block:
    # Objects that don't have unique metadata are a lot easier for our engine
    # to deal with. We only have to instantiate them once, saving ram.
    unique = False
    texture = None

    def destroy(self):
        pass


class Tool:
    pass


class Inventory:
    # Anyone or anything should be able to have an inventory
    pass


class Mob:
    pass
