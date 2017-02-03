from pycraft.util import normalize

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

    def get_block(self, coords):
        """get the block at the given `position`. This method assumes the
        block has already been added with add_block()

        Parameters
        ----------
        coords : tuple of len 3
            The (x, y, z) position of the block to show.
        """
        return self.blocks[coords] if self.blocks[coords] else None

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

    def get_neighbors(self, position):
        """Check all blocks surrounding `position` and ensure their visual
        state is current. This means hiding blocks that are not exposed and
        ensuring that all exposed blocks are shown. Usually used after a block
        is added or removed.
        """
        x, y, z = position
        neighbors = {
            'show': list(),
            'hide': list()
        }
        for dx, dy, dz in FACES:
            key = (x + dx, y + dy, z + dz)
            if key not in self.blocks:
                continue
            if self.exposed(key):
                neighbors['show'].append({
                    'coords': key,
                    'block': self.get_block(key)
                })
            else:
                neighbors['hide'].append({
                    'coords': key
                })
        return neighbors

    def hit_test(self, coords, vector, max_distance=8):
        """Line of sight search from current position. If a block is
        intersected it is returned, along with the block previously in the line
        of sight. If no block is found, return None, None.

        Parameters
        ----------
        coords : tuple of len 3
            The (x, y, z) position to check visibility from.
        vector : tuple of len 3
            The line of sight vector.
        max_distance : int
            How many blocks away to search for a hit.
        """
        m = 8
        x, y, z = coords
        dx, dy, dz = vector
        previous = None
        for _ in range(max_distance * m):
            key = normalize((x, y, z))
            if key != previous and key in self.blocks:
                return key, previous
            previous = key
            x, y, z = x + dx / m, y + dy / m, z + dz / m
        return None, None
