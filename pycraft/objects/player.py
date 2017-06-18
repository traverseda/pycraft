# python imports
import math

# project imports
from pycraft.objects.character import Character
from pycraft.objects.storage import Storage
from pycraft.util import normalize


class Player(Character):
    def __init__(self, config):
        super(Player, self).__init__(config)
        # Velocity in the y (upward) direction.
        self.dy = 0
        # A dict of player blocks with their respective quantities
        self.inventory = Storage()
        self.inventory.store_item(0, 'Brick', 5)
        self.inventory.store_item(1, 'Grass', 7)
        self.inventory.store_item(2, 'WeakStone', 10)
        self.inventory.store_item(3, 'Sand', 5)

        self.current_item = 'Brick'
        self.current_item_index = 0

    def get_block(self):
        item = self.inventory.retrieve_item(self.current_item)
        self.switch_inventory(self.current_item_index)
        if isinstance(item, dict):
            return item['item']
        return None

    def switch_inventory(self, index):
        """
        Change selected element in the inventory
        :param index:integer
        :return:None
        """
        self.current_item_index = index
        self.current_item = self.inventory.get_item_name(self.current_item_index)

    def get_sight_vector(self):
        """Returns the current line of sight vector indicating the direction the
        player is looking.
        """
        x, y = self.rotation
        # y ranges from -90 to 90, or -pi/2 to pi/2, so m ranges from 0 to 1 and
        # is 1 when looking ahead parallel to the ground and 0 when looking
        # straight up or down.
        m = math.cos(math.radians(y))
        # dy ranges from -1 to 1 and is -1 when looking straight down and 1 when
        # looking straight up.
        dy = math.sin(math.radians(y))
        dx = math.cos(math.radians(x - 90)) * m
        dz = math.sin(math.radians(x - 90)) * m
        return dx, dy, dz

    def hit(self, blocks, max_distance=8, left=True):
        """Line of sight search from current position. If a block is
        intersected it is returned, along with the block previously in the line
        of sight. If no block is found, return None, None.

        Parameters
        ----------
        blocks : dict
            A mapping from position to the texture of a block
        max_distance : int
            How many blocks away to search for a hit.
        left : bool
            hit is called by left-click or not
        """
        m = 8
        x, y, z = self.position
        head, feet = normalize((x, y, z)), normalize((x, y - 1, z))
        dx, dy, dz = self.get_sight_vector()
        previous = None
        for _ in range(max_distance * m):
            key = normalize((x, y, z))
            if key != previous and key in blocks:
                if not left and (previous == head or previous == feet):
                    continue
                # Make sure the block isn't the player's head or feet in case of adding.
                return key, previous
            previous = key
            x, y, z = x + dx / m, y + dy / m, z + dz / m
        return None, None
