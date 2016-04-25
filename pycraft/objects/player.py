# python imports
import math

# project imports
from pycraft.objects.character import Character


class Player(Character):
    def __init__(self, config):
        super(Player, self).__init__(config)
        # Velocity in the y (upward) direction.
        self.dy = 0
        # A dict of player blocks with their respective quantities
        self.items = {
            "Brick": {
                "qty": 10
            },
            "Grass": {
                "qty": 20
            },
            "Sand": {
                "qty": 5
            },
            "WeakStone": {
                "qty": 15
            }
        }

        # this way you only have to modify the dict to add items to the starting inventory
        self.inventory = list(self.items.keys())
        # The current block the user can place. Hit num keys to cycle.
        self.block = self.inventory[0]

    def switch_inventory(self, index):
        """
        Change selected element in the inventory
        :param index:integer
        :return:None
        """
        if len(self.inventory):
            self.block = self.inventory[index % len(self.inventory)]

    def adjust_inventory(self, item, qty=1):
        """
        Adjusts player inventory when a block is placed; updates current
        block if item is no longer available
        :param item:string
        :param qty:integer
        :return:None
        """
        self.items[item]["qty"] -= qty
        if self.items[item]["qty"] == 0:
            self.inventory.remove(item)
            del self.items[item]
            if self.block == item:
                self.block = self.inventory[0] if len(self.inventory) else None

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
