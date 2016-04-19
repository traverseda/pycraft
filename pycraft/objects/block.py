from pycraft.objects.object import WorldObject
from pycraft.objects.textures import tex_coords

GRASS = tex_coords((1, 0), (0, 1), (0, 0))
SAND = tex_coords((1, 1), (1, 1), (1, 1))
BRICK = tex_coords((2, 0), (2, 0), (2, 0))
STONE = tex_coords((2, 1), (2, 1), (2, 1))


class Block(WorldObject):

    unique = False
    texture = None

    def destroy(self):
        pass


class Brick(Block):
    texture = BRICK


class Grass(Block):
    texture = GRASS


class Sand(Block):
    texture = SAND


class Stone(Block):
    texture = STONE

    def destroy(self):
        pass
