from noise.perlin import SimplexNoise

from pycraft.objects import Sand, Grass, Stone
from pycraft.util import reverse_sectorize, sectorize

simplex_noise2 = SimplexNoise(256).noise2


class Sector:
    def __init__(self, area):
        self.area = area
        # A mapping from position to the texture of the block at that position.
        # This defines all the blocks that are currently in the sector.
        self.blocks = {}

    def change_sectors(self, before, after):
        """Move from sector `before` to sector `after`. A sector is a
        contiguous x, y sub-region of world. Sectors are used to speed up
        world rendering.
        """
        before_set = set()
        after_set = set()
        pad = 4
        for dx in range(-pad, pad + 1):
            for dy in [0]:  # range(-pad, pad + 1):
                for dz in range(-pad, pad + 1):
                    if dx ** 2 + dy ** 2 + dz ** 2 > (pad + 1) ** 2:
                        continue
                    if before:
                        x, y, z = before
                        before_set.add((x + dx, y + dy, z + dz))
                    if after:
                        x, y, z = after
                        after_set.add((x + dx, y + dy, z + dz))
        show = after_set - before_set
        hide = before_set - after_set
        for sector in show:
            self.show_sector(sector)
        for sector in hide:
            self.hide_sector(sector)

    def generate_sector(self, sector):
        """Generate blocks within sector using simplex_noise2
        """
        for column in reverse_sectorize(sector):
            x, z = column
            y_max = int((simplex_noise2(x / 30, z / 30) + 1) * 3)
            for y_lvl in range(0 - 2, y_max):
                self.add_block((x, y_lvl, z), Sand(), immediate=False)
            else:
                self.add_block((x, y_lvl, z), Grass(), immediate=False)
            # add the safety stone floor.
            # don't want anyone falling into the ether.
            self.add_block((x, 0 - 3, z), Stone(), immediate=False)

    def hide_sector(self, sector):
        """Ensure all blocks in the given sector that should be hidden are
        removed from the canvas.
        """
        for position in self.area.sectors.get(sector, []):
            if position in self.area.shown:
                self.area.hide_block(position, False)

    def show_sector(self, sector):
        """Ensure all blocks in the given sector that should be shown are drawn
        to the canvas.
        """
        positions = self.area.sectors.get(sector, [])
        if positions:
            for position in positions:
                if position not in self.area.shown and self.area.exposed(position):
                    self.area.show_block(position, False)
        else:
            self.generate_sector(sector)
            self.show_sector(sector)

    def add_block(self, position, texture, immediate=True):
        """Add a block with the given `texture` and `position` to the world.

        Parameters
        ----------
        position : tuple of len 3
            The (x, y, z) position of the block to add.
        texture : list of len 3
            The coordinates of the texture squares. Use `tex_coords()` to
            generate.
        immediate : bool
            Whether or not to draw the block immediately.
        """
        if position in self.area.objects:
            self.area.remove_block(position, immediate)
        self.area.objects[position] = texture
        self.area.sectors.setdefault(sectorize(position), []).append(position)
        if immediate:
            if self.area.exposed(position):
                self.area.show_block(position)
            self.area.check_neighbors(position)
