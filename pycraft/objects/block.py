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


class Brick(Block):
    id = 1
    texture = BRICK
    breakable = True


class Grass(Block):
    id = 2
    texture = GRASS
    breakable = True


class Sand(Block):
    id = 3
    texture = SAND
    breakable = True


class WeakStone(Block):
    id = 4
    texture = STONE
    breakable = True


class Stone(Block):
    id = 5
    texture = STONE
