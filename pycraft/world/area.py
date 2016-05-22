FACES = [
    (0, 1, 0),
    (0, -1, 0),
    (-1, 0, 0),
    (1, 0, 0),
    (0, 0, 1),
    (0, 0, -1),
]


class Area:
    def __init__(self):
        # A mapping from position to the texture of the block at that position.
        # This defines all the blocks that are currently in the world.
        self.blocks = {}


        # self.world = world
        # self.show_hide_queue = OrderedDict()

    def get_blocks(self):
        return self.blocks

    def add_block(self, coords, block):
        """
        Add a block element to blocks list
        Parameters
        ----------
        coords
        block

        Returns
        -------

        """
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
        # self.sectors[sectorize(coords)].remove(coords)
        # if immediate:
        #     if coords in self.shown:
        #         self.hide_block(coords)
        #     self.check_neighbors(coords)

    def get_block(self, coords):
        """Show the block at the given `position`. This method assumes the
        block has already been added with add_block()

        Parameters
        ----------
        coords : tuple of len 3
            The (x, y, z) position of the block to show.
        """
        return self.blocks[coords] if self.blocks[coords] else None
        # self.shown[coords] = block
        # if immediate:
        #     self.world.show_block(coords, block)
        # else:
        #     self.show_hide_queue[coords] = True

    def exposed(self, position):
        """Returns False is given `position` is surrounded on all 6 sides by
        blocks, True otherwise.
        Parameters
        ----------
        position

        Returns
        -------

        """
        x, y, z = position
        for dx, dy, dz in FACES:
            if (x + dx, y + dy, z + dz) not in self.blocks:
                return True
        return False
    #
    # def remove_block(self, position, immediate=True):
    #     """Remove the block at the given `position`.
    #
    #     Parameters
    #     ----------
    #     position : tuple of len 3
    #         The (x, y, z) position of the block to remove.
    #     immediate : bool
    #         Whether or not to immediately remove block from canvas.
    #     """
    #     del self.blocks[position]
    #     self.sectors[sectorize(position)].remove(position)
    #     if immediate:
    #         if position in self.shown:
    #             self.hide_block(position)
    #         self.check_neighbors(position)
    #
    # def check_neighbors(self, position):
    #     """Check all blocks surrounding `position` and ensure their visual
    #     state is current. This means hiding blocks that are not exposed and
    #     ensuring that all exposed blocks are shown. Usually used after a block
    #     is added or removed.
    #     """
    #     x, y, z = position
    #     for dx, dy, dz in FACES:
    #         key = (x + dx, y + dy, z + dz)
    #         if key not in self.blocks:
    #             continue
    #         if self.exposed(key):
    #             if key not in self.shown:
    #                 self.show_block(key)
    #         else:
    #             if key in self.shown:
    #                 self.hide_block(key)

    # def hide_block(self, position, immediate=True):
    #     """Hide the block at the given `position`. Hiding does not remove the
    #     block from the world.
    #
    #     Parameters
    #     ----------
    #     position : tuple of len 3
    #         The (x, y, z) position of the block to hide.
    #     immediate : bool
    #         Whether or not to immediately remove the block from the canvas.
    #     """
    #     self.shown.pop(position)
    #     if immediate:
    #         self.world.hide_block(position)
    #     else:
    #         self.show_hide_queue[position] = False
