"""
Unit tests for the util.py module.
"""
from pycraft.objects.storage import Storage


def test_create_storage():
    """
    Test cube_vertices function.
    """
    storage_obj = Storage()
    assert len(storage_obj.items) == 10, 'Default storage has 10 items'
    assert storage_obj.max_items == 10, 'Default storage max items are 10'
    assert isinstance(storage_obj.items, dict), 'Default storage items is a dictionary'


def test_storage_item():
    """
    Test cube_vertices function.
    """
    storage_obj = Storage()
    storage_obj.store_item(1, 'test')

    assert storage_obj.items[1] == {'test': 1}, 'Item in the position 1 coincide with the inserted item with value 1'
    assert storage_obj.items[0] == dict(), 'Item in the position 0 is empty'

    storage_obj.store_item(1, 'test')
    assert storage_obj.items[1] == {'test': 2}, 'Item in the position 1 coincide with the inserted item with value 2'

    assert storage_obj.store_item(10, 'test2') == False, "Can't store items in positions over max items"
    assert storage_obj.store_item(9, 'test2') == False, "Can store items in las position"


if __name__ == "__main__":
    test_create_storage()
    test_storage_item()
