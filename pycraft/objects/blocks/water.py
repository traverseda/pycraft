from ..textures import tex_coords
from ..block import Block

WATER = tex_coords((1, 0), (0, 1), (0, 0))


class Water(Block):
    id = 7
    texture = WATER
    breakable = True
    texture_path = 'pycraft/objects/texture/water.jpg'
