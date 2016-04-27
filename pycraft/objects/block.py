# python imports
import sys

# project imports
from .object import WorldObject
from .textures import tex_coords

GRASS = tex_coords((1, 0), (0, 1), (0, 0))
SAND = tex_coords((1, 1), (1, 1), (1, 1))
BRICK = tex_coords((2, 0), (2, 0), (2, 0))
STONE = tex_coords((2, 1), (2, 1), (2, 1))


class Block(WorldObject):
    texture_path = 'pycraft/objects/textures.png'
    durability = 1

    def __init__(self):
        self.block_duration = self.durability

    def hit_and_destroy(self):
        if not self.breakable:
            return False
        self.block_duration -= 1
        return self.block_duration == 0


def get_block(identifier):
    try:
        classname = globals()[identifier.capitalize()]
        return classname()
    except KeyError:
        sys.exit('Exiting! Class {} can\'t be instanciated'.format(identifier))


class Brick(Block):
    identifier = 'Brick'
    texture = BRICK
    breakable = True
    durability = 10


class Grass(Block):
    identifier = 'Grass'
    texture = GRASS
    breakable = True
    durability = 5


class Sand(Block):
    identifier = 'Sand'
    texture = SAND
    breakable = True
    durability = 2


class Weakstone(Block):
    identifier = 'Weakstone'
    texture = STONE
    breakable = True
    durability = 15


class Stone(Block):
    identifier = 'Stone'
    texture = STONE
