from .object import WorldObject
from .textures import tex_coords

GRASS = tex_coords((1, 0), (0, 1), (0, 0))
SAND = tex_coords((1, 1), (1, 1), (1, 1))
BRICK = tex_coords((2, 0), (2, 0), (2, 0))
STONE = tex_coords((2, 1), (2, 1), (2, 1))


class Block(WorldObject):
    unique = False
    texture = None
    breakable = False
    texture_path = 'pycraft/objects/textures.png'
    durability = 1

    def __init__(self):
        self.block_duration = self.durability

    def hit_and_destroy(self):
        if not self.breakable:
            return False
        self.block_duration -= 1
        return self.block_duration == 0


class Brick(Block):
    id = 1
    texture = BRICK
    breakable = True
    durability = 10


class Grass(Block):
    id = 2
    texture = GRASS
    breakable = True
    durability = 5


class Sand(Block):
    id = 3
    texture = SAND
    breakable = True
    durability = 2


class WeakStone(Block):
    id = 4
    texture = STONE
    breakable = True
    durability = 15


class Stone(Block):
    id = 5
    texture = STONE
