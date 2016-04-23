"""
Unit tests for the util.py module.
"""
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pycraft.util as util


def test_cube_vertices():
    """
    Test cube_vertices function.
    """
    # After looking through this function, I really don't understand what it is supposed to be
    # doing. There are many repeated vertices being generated and little organization. I don't
    # want to mess anything up that other parts of the code are relying on so maybe someone
    # else should take a look this.
    # print(util.cube_vertices(0, 10, 20, 1))

def test_normalize():
    """
    Test the normalize function.
    """
    my_pos = [3.29, 5.9, 7.001]
    expected = [3, 6, 7]
    norm_pos = util.normalize(my_pos)
    for i, e in zip(norm_pos, expected):
        assert isinstance(i, int), "Returned position not an integer"
        assert i == e, "Returned postion ({}) not what we expected ({})!".format(i, e)

def test_sectorize():
    """
    Test the sectorize function.
    Currently assumes sector_size is 16, should make this not hard coded!
    """
    sector_size = 16
    my_pos = [65, 30, 65]
    expected = [4, 0, 4]
    sector = util.sectorize(my_pos)
    for i, e in zip(sector, expected):
        assert i == e, "Returned sector not what was expected"


if __name__ == "__main__":
    test_cube_vertices()
    test_normalize()
    test_sectorize()
