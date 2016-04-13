from pycraft.objects.object import WorldObject, WorldObjectRegistry
from pycraft.objects.textures import tex_coords

GRASS = tex_coords((1, 0), (0, 1), (0, 0))
SAND = tex_coords((1, 1), (1, 1), (1, 1))
BRICK = tex_coords((2, 0), (2, 0), (2, 0))
STONE = tex_coords((2, 1), (2, 1), (2, 1))

objects = WorldObjectRegistry('blocks')


class Block(WorldObject):

    unique = False
    texture = None

    def destroy(self):
        pass


@objects.register('brick')
class Brick(Block):
    texture = BRICK


@objects.register('grass')
class Grass(Block):
    texture = GRASS


@objects.register('sand')
class Sand(Block):
    texture = SAND


@objects.register('stone')
class Stone(Block):
    texture = STONE

    def destroy(self):
        pass
