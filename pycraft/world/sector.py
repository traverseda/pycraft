from noise.perlin import SimplexNoise

from pycraft.objects import Sand, Grass, Stone
from pycraft.util import reverse_sectorize

simplex_noise2 = SimplexNoise(256).noise2


class Sector:
    def __init__(self, coords, area):
        self.area = area
        # A mapping from position to the texture of the block at that position.
        # This defines all the blocks that are currently in the sector.
        self.blocks = {}

        self.generate_sector(coords)

    def add_block(self, coords, block):
        """Add a block with the given `texture` and `position` to the world.

        Parameters
        ----------
        coords : tuple of len 3
            The (x, y, z) position of the block to add.
        block : list of len 3
            The coordinates of the texture squares. Use `tex_coords()` to
            generate.
        """
        self.area.add_block(coords, block)
        if coords in self.blocks:
            self.remove_block(coords)
        self.blocks[coords] = block

    def remove_block(self, coords):
        """Remove the block at the given `coords`.

        Parameters
        ----------
        coords : tuple of len 3
            The (x, y, z) position of the block to remove.
        """
        del self.blocks[coords]

    def generate_sector(self, coords):
        """Generate blocks within sector using simplex_noise2
        """
        for column in reverse_sectorize(coords):
            x, z = column
            y_max = int((simplex_noise2(x / 30, z / 30) + 1) * 3)
            for y_lvl in range(0 - 2, y_max):
                self.add_block((x, y_lvl, z), Sand())
            else:
                self.add_block((x, y_lvl, z), Grass())
            # add the safety stone floor.
            # don't want anyone falling into the ether.
            self.add_block((x, 0 - 3, z), Stone())
