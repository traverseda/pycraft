# python imports


# project imports


class Storage:
    def __init__(self):
        self.max_items = 10
        self.items = dict()
        self.start_storage()

    def start_storage(self):
        """
        Initializes the storage items
        Returns None
        -------

        """
        for x in range(0, self.max_items):
            self.items[x] = dict()

    def store_item(self, position, item, quantity=1):
        """
        Add items to the storage object
        Parameters
        ----------
        position integer
        item     object
        quantity integer

        Returns Boolean
        -------

        """
        if position >= self.max_items:
            return False

        if item in self.items[position]:
            self.items[position][item] += quantity
        else:
            self.items[position][item] = quantity
        return True

    def retrieve_item(self, position, quantity=1):
        """
        Retrieve an item from the storage
        Parameters
        ----------
        position
        quantity

        Returns
        -------

        """
        if position in self.items:
            items = self.items[position].items()
            for item, value in items:
                if value > 1:
                    self.items[position][item] -= 1
                    return item
                self.items[position].clear()
        return False
