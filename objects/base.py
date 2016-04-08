'''
This file should contain only the "base" class for blocks/tools/players/mobs

Essentially, they're abstract base classes. Put example objects in "default.py".

This is so that mods can remove default objects from their game.
'''

from collections import defaultdict

uids=defaultdict(lambda: None)

class Block(object):
    unique=False #Objects that don't have unique metadata are a lot easier for our engine to deal with. We only have to instantiate them once, saving ram.
    texture=None
    def getTexture(self):
        return self.texture
    def destroy(self):
        pass
    def getID(self):
        pass

class tool(object):
    pass

#Anyone or anything should be able to have an inventory
class inventory(object):
    pass

class mob(object):
    def __init__(self, *args,**kwargs):
        super( mob, self ).__init__(*args,**kwargs)
        
