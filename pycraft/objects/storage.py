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

    def get_item_name(self, active=0):
        """
        Retrieve the name of an item in the storage from an index
        Parameters
        ----------
        active

        Returns
        -------

        """
        if active >= self.max_items:
            active = 0

        if self.items[active]:
            return [item for item in self.items[active]][0]
        return False

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

    def retrieve_item_by_position(self, position, quantity=1):
        """
        Retrieve an item from the storage by position
        Parameters
        ----------
        position
        quantity

        Returns
        -------

        """
        if position in self.items:
            items = self.items[position].copy().items()
            for item, value in items:
                if value > quantity:
                    self.items[position][item] -= quantity
                else:
                    quantity = value
                    self.items[position].clear()
                return {
                    "item": item,
                    "quantity": quantity
                }

        return False

    def retrieve_item(self, item, quantity=1):
        """
        Retrieve an item from the storage
        Parameters
        ----------
        item
        quantity

        Returns
        -------

        """
        items = self.items.copy().items()
        for key, value in items:
            if item in value:
                if value[item] > quantity:
                    self.items[key][item] -= quantity
                else:
                    quantity = value[item]
                    self.items[key].clear()

                return {
                    "item": item,
                    "quantity": quantity
                }

        return False
