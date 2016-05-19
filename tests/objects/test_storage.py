"""
Unit tests for the util.py module.
"""
from pycraft.objects.storage import Storage


def test_create_storage():
    """
    Test create storage.
    """
    storage_obj = Storage()
    assert len(storage_obj.items) == 10, 'Default storage has 10 items'
    assert storage_obj.max_items == 10, 'Default storage max items are 10'
    assert isinstance(storage_obj.items, dict), 'Default storage items is a dictionary'


def test_storage_item():
    """
    Test store_item function.
    """
    storage_obj = Storage()
    storage_obj.store_item(1, 'test')

    assert storage_obj.items[1] == {'test': 1}, 'Item in the position 1 coincide with the inserted item with value 1'
    assert storage_obj.items[0] == dict(), 'Item in the position 0 is empty'

    storage_obj.store_item(1, 'test')
    assert storage_obj.items[1] == {'test': 2}, 'Item in the position 1 coincide with the inserted item with value 2'

    assert storage_obj.store_item(10, 'test2') is False, "Can't store items in positions over max items"
    assert storage_obj.store_item(9, 'test2') is True, "Can store items in last position"

    storage_obj.store_item(2, 'test', 3)
    assert storage_obj.items[2] == {'test': 3}, 'Item in the position 2 coincide with the inserted item with value 3'


def test_retrieve_item_by_position():
    """
    Test store_item function.
    """
    storage_obj = Storage()
    storage_obj.store_item(1, 'test')

    data_test_1 = {"item": 'test', "quantity": 1}

    assert storage_obj.retrieve_item_by_position(1) == data_test_1, \
        'Item in the position 1 coincide with the item with value 1'
    assert storage_obj.retrieve_item_by_position(1) is False, 'Item in the position 1 is empty'

    data_test_2 = {"item": 'test', "quantity": 2}

    storage_obj.store_item(2, 'test', 3)
    assert storage_obj.retrieve_item_by_position(2, 2) == data_test_2, \
        'Item in the position 2 coincide with the item with value 2'


def test_retrieve_item():
    """
    Test store_item function.
    """
    storage_obj = Storage()
    storage_obj.store_item(1, 'test')

    data_test_1 = {"item": 'test', "quantity": 1}

    assert storage_obj.retrieve_item('test') == data_test_1, \
        'Item in the position 1 coincide with the item with value 1'
    assert storage_obj.retrieve_item('test') is False, 'Item in the position 1 is empty'

    data_test_2 = {"item": 'test', "quantity": 2}
    #
    storage_obj.store_item(2, 'test', 3)
    assert storage_obj.retrieve_item('test', 2) == data_test_2, \
        'Item in the position 2 coincide with the item with value 2'


def test_next_item():
    """
    Test store_item function.
    """
    storage_obj = Storage()
    storage_obj.store_item(0, 'test')

    assert storage_obj.get_item_name() == 'test', 'Retrieve the name of the first item in the storage'

    storage_obj = Storage()
    storage_obj.store_item(1, 'test')

    assert storage_obj.get_item_name() is False, 'Fails to retrieve the name of the first item in the storage'

    assert storage_obj.get_item_name(10) is False, 'Fails to retrieve the name with and index over max storage'


if __name__ == "__main__":
    test_create_storage()
    test_storage_item()
    test_retrieve_item_by_position()
    test_retrieve_item()
    test_next_item()
